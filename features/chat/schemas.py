from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="The message to echo back"
    )


class EchoResponse(BaseModel):
    echo: str = Field(
        ...,
        description="The echoed message"
    )
