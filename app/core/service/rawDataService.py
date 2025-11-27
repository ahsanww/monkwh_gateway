from fastapi import APIRouter
from app.utils import util
from pydantic import BaseModel
from app.data.Constant import STATUS_API

router = APIRouter(prefix="/rawdata", tags=["Raw Data"])


class HexPayload(BaseModel):
    payload: str  # e.g. "0xFF 0xAA 0xBB"


@router.post("/send")
async def send_raw_data(data: dict):
    try:
        hex_str = data["payload"]
        return {
            "msg": hex_str,
            "timestamp": util.create_timeStamp(),
            "status": int(STATUS_API.OK),
        }
    except ValueError as e:
        return {
            "status": int(STATUS_API.ERROR),
            "error": f"Invalid hex string: {str(e)}",
        }


@router.post("/check")
async def get_raw_data(bytesData):
    return {"message": "Raw data inserted"}
