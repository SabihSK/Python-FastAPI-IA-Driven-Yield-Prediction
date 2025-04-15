from fastapi import APIRouter
from features.auth.routes import router as auth_router
from features.chat.routes import router as chat_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(chat_router, prefix="/chat", tags=["Chat"])
