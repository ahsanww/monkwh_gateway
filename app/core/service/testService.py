from fastapi import APIRouter, Depends
from app.core.database.db import get_db
from app.core.logic import testLogic
from datetime import datetime

router = APIRouter(prefix="/test", tags=["TEST"])


@router.post("/dummy")
async def inserDummyLoadProfile(
    idPelanggan, serialNumber, profileDate, conn=Depends(get_db)
):
    profile_date = datetime.strptime(profileDate, "%Y-%m-%d").date()
    rows = testLogic.generate_96_rows(
        id_pelanggan=idPelanggan,
        serial_number=serialNumber,
        profile_date=datetime.strptime(profileDate, "%Y-%m-%d").date(),
    )
    async with conn.transaction():
        # ✅ WAJIB: pastikan partition ada
        await conn.execute("SELECT public.create_it_kwh_lp_partition($1)", profile_date)

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
    return_data = {"status": 200, "error": None}

    return return_data
