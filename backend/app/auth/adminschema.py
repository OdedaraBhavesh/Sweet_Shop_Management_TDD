# app/schemas.py

from pydantic import BaseModel, EmailStr


class AdminLogin(BaseModel):
    email: EmailStr
    hashed_password: str
