"""_summary_"""

from fastapi import Header, HTTPException, status
from core.config import API_KEY


async def api_key_auth(api_key: str = Header(...)):
    """_summary_"""
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
