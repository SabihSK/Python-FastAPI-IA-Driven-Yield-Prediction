"""_summary_"""
from fastapi import APIRouter
from features.auth.routes import router as auth_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
