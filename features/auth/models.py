"""_summary_"""
from sqlalchemy import Column, Integer, String
from core.db import Base


class User(Base):
    """_summary_"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
