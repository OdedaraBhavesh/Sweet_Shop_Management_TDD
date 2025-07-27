from pydantic import BaseModel
from typing import Optional


class AddToCartModel(BaseModel):
    sweet_id: str
    quantity: int
