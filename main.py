"""_summary_

Yields:
    _type_: _description_
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- Your React frontend
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)

app.include_router(api_router)
