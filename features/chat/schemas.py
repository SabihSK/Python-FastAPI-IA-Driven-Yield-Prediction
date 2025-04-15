from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="The message to echo back"
        )
