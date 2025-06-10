import os
import ssl
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(subject: str, body: str, to: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to
    msg.set_content(body)

    context = ssl.create_default_context()
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
    try:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    finally:
        smtp.quit()
