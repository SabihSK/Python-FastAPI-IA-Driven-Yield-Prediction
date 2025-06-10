from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from core.email_service import send_email

router = APIRouter()


class EmailRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str
    category: str  # e.g., General, Feedback, etc.
    message: str


@router.post("/send-email")
async def send_email_endpoint(data: EmailRequest):
    try:
        composed_subject = f"[{data.category}] {data.subject}"
        composed_body = f"""
You have a new message from the contact form:

Name: {data.name}
Email: {data.email}
Category: {data.category}
Subject: {data.subject}

Message:
{data.message}
        """

        send_email(
            subject=composed_subject, body=composed_body, to="m.aleydev@gmail.com"
        )
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
