"""_summary_"""
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(name: str, email: str, password: str, db: AsyncSession):
    """_summary_"""
    hashed_password = pwd_context.hash(password)
    user = User(name=name, email=email, password=hashed_password)

    db.add(user)
    try:
        await db.commit()
        await db.refresh(user)
        return {"id": user.id, "name": user.name, "email": user.email}
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already exists",
            ) from exc


async def login_user(email: str, password: str, db: AsyncSession):
    """_summary_"""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if user and pwd_context.verify(password, user.password):
        return {
            "message": "Login successful",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
            },
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")
