from fastapi import APIRouter, HTTPException
from app.core.database.db import get_db
from app.utils import util
from typing import Optional
from datetime import date, timedelta, datetime
from fastapi import Depends
import random

router = APIRouter(prefix="/data", tags=["Data"])


# @router.get("/loadProfile")
# async def getLoadProfile(
#     id_pelanggan,
#     meterNumber,
#     mode: bool = True,
#     startDate: Optional[date] = None,
#     endDate: Optional[date] = None,
#     index: Optional[int] = None,
# ):
#     if mode:
#         return {
#             "mode": "all",
#             "message": "Mode true → parameter tanggal & index diabaikan",
#         }

#     # mode == False
#     if index is None and (startDate is None or endDate is None):
#         raise HTTPException(
#             status_code=400,
#             detail="Jika mode=false, wajib isi index ATAU startDate & endDate",
#         )

#     start = datetime.strptime("00:00", "%H:%M")
#     dummy_data = [
#         {
#             "time": (start + timedelta(minutes=15 * i)).strftime("%H:%M"),
#             "kwh": 1000.0 + i,
#             "kvarh": 200.0 + i,
#             "kw": 10.0 + (i * 0.1),
#             "kva": 12.0 + (i * 0.1),
#             "pf": 0.95,
#             "voltage_l1": 230.0,
#             "voltage_l2": 231.0,
#             "voltage_l3": 232.0,
#             "current_l1": 5.0,
#             "current_l2": 5.1,
#             "current_l3": 5.2,
#             "event": "none",
#         }
#         for i in range(index)
#     ]
#     return_data = {}
#     if len(dummy_data) == index:
#         return_data = {
#             "id_pelanggan": id_pelanggan,
#             "meterSerialNumber": meterNumber,
#             "startDate": startDate,
#             "endDate": endDate,
#             "dataIndex": index,
#             "data": dummy_data,
#             "status": 200,
#             "error": "none",
#         }
#     else:
#         return_data = {
#             "id_pelanggan": id_pelanggan,
#             "meterSerialNumber": meterNumber,
#             "startDate": startDate,
#             "endDate": endDate,
#             "dataIndex": index,
#             "data": [],
#             "status": 404,
#             "error": "index data not same",
#         }
#     return return_data


@router.get("/loadProfile")
async def getLoadProfile(
    id_pelanggan: str,
    meterNumber: str,
    mode: bool = True,
    startDate: Optional[date] = None,
    endDate: Optional[date] = None,
    index: Optional[int] = None,
    conn=Depends(get_db),
):
    # ======================
    # MODE TRUE → LATEST DAY
    # ======================
    if mode:
        sql = """
                SELECT
                    idx,
                    to_char(time_slot, 'HH24:MI') AS time,
                    wh, varh,
                    v1, v2, v3,
                    a1, a2, a3,
                    event
                FROM public.it_kwh_load_profile
                WHERE serial_number = $1
                AND profile_date = (
                    SELECT MAX(profile_date)
                    FROM public.it_kwh_load_profile
                    WHERE serial_number = $1
                )
                ORDER BY idx
            """
        rows = await conn.fetch(sql, meterNumber)

        return {
            "mode": "all",
            "id_pelanggan": id_pelanggan,
            "meterSerialNumber": meterNumber,
            "data": [dict(r) for r in rows],
            "status": 200,
            "error": "none",
        }

    # ======================
    # MODE FALSE → VALIDASI
    # ======================
    if index is None and (startDate is None or endDate is None):
        raise HTTPException(
            status_code=400,
            detail="Jika mode=false, wajib isi index ATAU startDate & endDate",
        )

    # ======================
    # MODE FALSE → INDEX
    # ======================
    if index is not None:
        sql = """
                SELECT
                    idx,
                    to_char(time_slot, 'HH24:MI') AS time,
                    wh, varh,
                    v1, v2, v3,
                    a1, a2, a3,
                    event
                FROM public.it_kwh_load_profile
                WHERE serial_number = $1
                AND idx = $2
                ORDER BY profile_date DESC
                LIMIT 1
            """
        rows = await conn.fetch(sql, meterNumber, index)

    # ======================
    # MODE FALSE → DATE RANGE
    # ======================
    else:
        sql = """
                SELECT
                    idx,
                    to_char(time_slot, 'HH24:MI') AS time,
                    wh, varh,
                    v1, v2, v3,
                    a1, a2, a3,
                    event
                FROM public.it_kwh_load_profile
                WHERE serial_number = $1
                AND profile_date BETWEEN $2 AND $3
                ORDER BY profile_date, idx
            """
        rows = await conn.fetch(sql, meterNumber, startDate, endDate)

    # ======================
    # RESPONSE
    # ======================
    if not rows:
        return {
            "mode": "specific",
            "id_pelanggan": id_pelanggan,
            "meterSerialNumber": meterNumber,
            "startDate": startDate,
            "endDate": endDate,
            "dataIndex": index,
            "data": [],
            "status": 404,
            "error": "data not found",
        }

    return {
        "mode": "specific",
        "id_pelanggan": id_pelanggan,
        "meterSerialNumber": meterNumber,
        "startDate": startDate,
        "endDate": endDate,
        "dataIndex": index,
        "data": [dict(r) for r in rows],
        "status": 200,
        "error": "none",
    }


@router.get("/monthlyProfile")
async def getMonthlyProfile(id_pelanggan, meterNumber, tanggal: date):
    # dummy_data = [random.random()]
    indexData = 131
    data = [random.randint(0, 10000) for _ in range(indexData)]

    cooked_data = {
        "id_pelanggan": id_pelanggan,
        "meterSerialNumber": meterNumber,
        "date": tanggal,
        "dataIndex": indexData,
        "data": data,
        "status": 200,
        "error": "none",
    }
    return cooked_data
