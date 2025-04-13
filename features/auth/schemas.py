"""_summary_"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from .validators import validate_email, validate_password


class UserSignup(BaseModel):
    """_summary_"""
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator("email")
    @classmethod
    def email_validation(cls, v):
        """_summary_"""
        return validate_email(v)

    def __init__(self, **data):
        """_summary_"""
        super().__init__(**data)
        self.password = validate_password(self.password)


class UserLogin(BaseModel):
    """_summary_"""
    email: EmailStr
    password: str
