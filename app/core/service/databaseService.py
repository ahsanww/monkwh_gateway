from fastapi import APIRouter, Depends
from app.core.database.db import get_db
from app.utils import util
from typing import Optional

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/")
async def get_items(id_pelanggan, conn=Depends(get_db)):
    try:
        query = f"SELECT kwh_name FROM im_kwh WHERE id_pelanggan='{id_pelanggan}'"
        rows = await conn.fetch(query)
        respon = util.create_return(200, util.create_timeStamp(), "none", rows)
    except:
        respon = util.create_return(404, util.create_timeStamp(), "none", rows)
    finally:
        return respon


@router.post("/")
async def create_item(
    name: str, description: Optional[str] = None, conn=Depends(get_db)
):
    row = await conn.fetchrow(
        """
        INSERT INTO items (name, description)
        VALUES ($1, $2)
        RETURNING id, name, description;
        """,
        name,
        description,
    )
    return dict(row)
