import asyncpg
import os
from dotenv import load_dotenv
from fastapi import Depends

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


class Database:
    pool: asyncpg.pool.Pool = None


db = Database()


async def connect_to_db():
    """Try to connect but do NOT stop FastAPI if fails."""
    try:
        db.pool = await asyncpg.create_pool(
            DATABASE_URL, min_size=1, max_size=10, timeout=5
        )
        print("✅ DB Connected")
    except Exception as e:
        print(f"⚠️ WARNING: Cannot connect to DB at startup: {e}")
        print("➡️ FastAPI will continue running without DB.")
        db.pool = None


async def close_db_connection():
    await db.pool.close()
    print("Closed PostgreSQL connection")


async def get_db():
    if db.pool is None:
        raise Exception("Database pool is not initialized")
    async with db.pool.acquire() as connection:
        yield connection
