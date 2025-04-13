"""_summary_"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db

from .schemas import UserLogin, UserSignup
from .services import create_user, login_user

router = APIRouter()


@router.post("/signup")
async def signup(user: UserSignup, db: AsyncSession = Depends(get_db)):
    """_summary_"""
    return await create_user(user.name, user.email, user.password, db)


@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    """_summary_"""
    return await login_user(user.email, user.password, db)
