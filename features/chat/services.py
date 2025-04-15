from .schemas import ChatMessage


async def echo_message(message: ChatMessage) -> dict:
    return {"echo": message.text}
