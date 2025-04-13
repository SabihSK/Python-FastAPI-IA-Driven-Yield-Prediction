"""_summary_

Yields:
    _type_: _description_
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routes import router as api_router
from core.db import Base, engine


@asynccontextmanager
async def lifespan(_app: FastAPI):  # renamed from app to _app
    """Startup logic"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield  # App runs here

    # Shutdown logic (optional)
    # await engine.dispose()  # if you need to close engine manually


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
