from datetime import date
from app.core.database.db import get_db
from app.core.database.db import connect_to_db, close_db_connection
from datetime import datetime, timedelta
import random

connect_to_db()
print("Database pool initialized")


def generate_96_rows(id_pelanggan, serial_number, profile_date):
    base_time = datetime.strptime("00:00", "%H:%M")
    rows = []

    for i in range(96):
        rows.append(
            (
                id_pelanggan,
                serial_number,
                profile_date,
                i + 1,
                (base_time + timedelta(minutes=15 * i)).time(),
                round(random.uniform(0, 50), 3),  # wh
                round(random.uniform(0, 20), 3),  # varh
                round(random.uniform(220, 240), 2),  # v1
                round(random.uniform(220, 240), 2),  # v2
                round(random.uniform(220, 240), 2),  # v3
                round(random.uniform(0, 100), 3),  # a1
                round(random.uniform(0, 100), 3),  # a2
                round(random.uniform(0, 100), 3),  # a3
                None,
            )
        )

    return rows


async def insert_load_profile(pool, id_pelanggan, serial_number, profile_date):
    rows = generate_96_rows(
        id_pelanggan=id_pelanggan,
        serial_number=serial_number,
        profile_date=profile_date,
    )

    async with pool.acquire() as conn:
        async with conn.transaction():
            # ✅ WAJIB: pastikan partition ada
            await conn.execute(
                "SELECT public.create_it_kwh_lp_partition($1)", profile_date
            )

            # ✅ BULK INSERT (COPY-like speed)
            await conn.executemany(
                """
                INSERT INTO public.it_kwh_load_profile (
                    id_pelanggan,
                    serial_number,
                    profile_date,
                    idx,
                    time_slot,
                    wh,
                    varh,
                    v1, v2, v3,
                    a1, a2, a3,
                    event
                ) VALUES (
                    $1,$2,$3,$4,$5,
                    $6,$7,$8,$9,$10,
                    $11,$12,$13,$14
                )
                ON CONFLICT (serial_number, profile_date, time_slot)
                DO NOTHING
            """,
                rows,
            )


close_db_connection()
print("Database pool closed")
