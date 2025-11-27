import asyncpg
from config import DATABASE_URL

db_pool = None


async def connect_to_db():
    global db_pool
    if db_pool is None:
        db_pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=2,
            max_size=10,
        )
    return db_pool


async def close_db_connection():
    global db_pool
    if db_pool:
        await db_pool.close()


async def query_data(query):
    global db_pool
    conn = db_pool.get_conn()
    try:
        with conn.cursor() as cursor:  # Automatically closes cursor
            cursor.execute(query)
            result = cursor.fetchall()
            conn.commit()  # Only needed for write operations
            return result
    except Exception as e:
        print(f"Query failed: {e}")
        conn.rollback()  # Good practice to rollback on error
        raise  # Re-raise the exception after handling
    finally:
        db_pool.release(conn)  # Ensure connection is always released


async def query_data_one(query):
    conn = db_pool.get_conn()
    try:
        with conn.cursor() as cursor:  # Automatically closes cursor
            cursor.execute(query)
            result = cursor.fetchone()
            conn.commit()  # Only needed for write operations
            return result
    except Exception as e:
        print(f"Query failed: {e}")
        conn.rollback()  # Good practice to rollback on error
        raise  # Re-raise the exception after handling
    finally:
        db_pool.release(conn)  # Ensure connection is always released
