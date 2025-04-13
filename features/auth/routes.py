"""_summary_"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from core.security import api_key_auth

from .schemas import UserLogin, UserSignup
from .services import create_user, login_user

router = APIRouter()


@router.post("/signup")
async def signup(
    user: UserSignup,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(api_key_auth),
):
    """Signup a new user"""
    return await create_user(user.name, user.email, user.password, db)


@router.post("/login")
async def login(
    user: UserLogin,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(api_key_auth),
):
    """Login an existing user"""
    return await login_user(user.email, user.password, db)
