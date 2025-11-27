from fastapi import APIRouter, Depends
from app.core.database.db import get_db
from app.utils import util
from typing import Optional
from datetime import date
import random

router = APIRouter(prefix="/data", tags=["Data"])


@router.get("/loadProfile")
async def getLoadProfile(id_pelanggan, meterNumber, tanggal: date, index: int):
    dummy_data = [
        {
            "index": i + 1,
            "kwh": 1000.0 + i,
            "kvarh": 200.0 + i,
            "kw": 10.0 + (i * 0.1),
            "kva": 12.0 + (i * 0.1),
            "pf": 0.95,
            "voltage_l1": 230.0,
            "voltage_l2": 231.0,
            "voltage_l3": 232.0,
            "current_l1": 5.0,
            "current_l2": 5.1,
            "current_l3": 5.2,
            "event": "none",
        }
        for i in range(index)
    ]
    cooked_data = {
        "id_pelanggan": id_pelanggan,
        "meterSerialNumber": meterNumber,
        "date": tanggal,
        "dataIndex": index,
        "data": dummy_data,
        "status": 200,
        "error": "none",
    }
    return cooked_data


# try:

# except:

# finally:
#     return respon


@router.post("/monthlyProfile")
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
