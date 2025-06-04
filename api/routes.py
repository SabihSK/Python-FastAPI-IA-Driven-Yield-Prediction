from fastapi import APIRouter
from features.auth.routes import router as auth_router
from features.irrigation.routes import router as irrigation_router
from features.yield_prediction.routes import router as yield_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(irrigation_router, prefix="/irrigation", tags=["Irrigation"])
router.include_router(yield_router)
