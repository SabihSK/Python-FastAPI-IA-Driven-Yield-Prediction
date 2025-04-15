from fastapi import APIRouter, Depends
from core.security import api_key_auth  # Optional: Secure with API Key
from .schemas import ChatMessage
from .services import echo_message

router = APIRouter()


@router.post("/echo", summary="Echo back the user's message")
async def echo(chat: ChatMessage, _: str = Depends(api_key_auth)):
    return await echo_message(chat)
