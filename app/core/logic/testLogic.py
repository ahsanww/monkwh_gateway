from datetime import date
from datetime import datetime, timedelta
import random


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
