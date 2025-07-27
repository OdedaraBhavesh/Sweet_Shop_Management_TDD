from pydantic import BaseModel
from typing import List


class CartItem(BaseModel):
    sweet_id: str
    quantity: int


class CartOutItem(BaseModel):
    sweet_id: str
    quantity: int


class UpdateCartQuantity(BaseModel):
    quantity: int
