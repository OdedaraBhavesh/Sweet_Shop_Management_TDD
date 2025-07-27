# app/models.py

from pydantic import BaseModel, EmailStr
from typing import List


class Admin(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    role: str = "admin"
    permissions: List[str] = [
        "create_sweets",
        "update_sweets",
        "delete_sweets",
        "restock_sweets"
    ]
