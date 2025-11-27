# app/main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.core.database.db import connect_to_db, close_db_connection
from app.core.service import (
    downlinkService,
    rawDataService,
    databaseService,
    dataService,
)


async def lifespan(app: FastAPI):
    # Startup
    await connect_to_db()
    print("Database pool initialized")

    yield  # FastAPI runs app here

    # Shutdown
    await close_db_connection()
    print("Database pool closed")


app = FastAPI(title="MonKwh API", lifespan=lifespan, docs_url="api/monkwh")


# Redirect root (/) ke /docs
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/monkwh")


# Include all routers
app.include_router(downlinkService.router)
app.include_router(rawDataService.router)
app.include_router(databaseService.router)
app.include_router(dataService.router)

# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
