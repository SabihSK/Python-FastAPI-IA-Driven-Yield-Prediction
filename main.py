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


app = FastAPI(
    lifespan=lifespan,
    title="AI-Driven Wheat Yield Prediction & Crop Management System",
    description="""
    🌾 This system helps farmers make data-informed decisions about crop management, irrigation, and wheat yield prediction.

    🚀 Features:
    - Location-based irrigation requirement
    - Crop planning and chemical recommendations
    - Yield forecasting using machine learning
    - User-specific crop tracking with analytics
    """,
    version="1.0.0",
    contact={
        "name": "AI-Driven Solutions",
        "url": "https://wheat-yield-pwa-fyp.vercel.app",
        "email": "wareesha.g20496@iqra.edu.pk",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:3000"],  # <-- Your React frontend
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)

app.include_router(api_router)
