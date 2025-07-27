# app/schemas/inventory.py
from pydantic import BaseModel, Field


class InventoryUpdate(BaseModel):
    amount: int = Field(gt=0, description="Quantity to increase or decrease")
