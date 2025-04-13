"""_summary_"""
import re


def validate_password(password: str):
    """_summary_"""
    if (
        len(password) < 8
        or not re.search(r"[A-Z]", password)
        or not re.search(r"[a-z]", password)
        or not re.search(r"\d", password)
        or not re.search(r"[@$!%*?&]", password)
    ):
        raise ValueError(
            (
                "Password must be at least 8 characters and include uppercase,"
                " lowercase, digit, and special char."
            )
        )
    return password


def validate_email(email: str):
    """_summary_"""
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, email):
        raise ValueError("Invalid email format")
    return email
