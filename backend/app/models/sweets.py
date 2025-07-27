# app/models/sweet.py

from pydantic import BaseModel, Field
from typing import Optional


class SweetBase(BaseModel):
    name: str = Field(..., example="Kaju Katli")
    description: Optional[str] = Field(
        None, example="Made with cashews and sugar")
    price: float = Field(..., example=300.0)
    quantity: int = Field(..., example=50)
    category: Optional[str] = Field(
        None, example="Traditional")  # ✅ New field added


class SweetCreate(SweetBase):
    pass


class SweetUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    quantity: Optional[int]
    category: Optional[str]  # ✅ Allow updates to category too


class SweetOut(SweetBase):
    id: str
    category: Optional[str] = Field(
        None, example="Traditional")  # ✅ Include in output
