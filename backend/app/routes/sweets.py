from fastapi import APIRouter, HTTPException, Depends, Query
from bson import ObjectId
from typing import Optional, List

from ..models.sweets import SweetCreate, SweetOut, SweetUpdate
from ..config.db import db
from ..auth.dependencies import get_current_user
from ..auth.dependencies import get_current_admin  # User auth dependency
from pydantic import BaseModel

router = APIRouter(prefix="/sweets", tags=["Sweets"])
sweets_collection = db["sweets"]

# -----------------------------
# Pydantic model for restocking
# -----------------------------


class RestockRequest(BaseModel):
    quantity: int

# -----------------------------
# Create a sweet (User Required)
# -----------------------------


@router.post("/", response_model=SweetOut)
async def create_sweet(sweet: SweetCreate, user=Depends(get_current_user)):
    sweet_dict = sweet.dict()
    result = await sweets_collection.insert_one(sweet_dict)
    sweet_dict["id"] = str(result.inserted_id)
    return SweetOut(**sweet_dict)

# -----------------------------
# List all sweets (Public)
# -----------------------------


@router.get("/", response_model=List[SweetOut])
async def list_sweets():
    sweets = []
    async for sweet in sweets_collection.find():
        sweet["id"] = str(sweet["_id"])
        sweet.pop("_id")
        sweets.append(SweetOut(**sweet))
    return sweets

# -----------------------------
# Search sweets (Public)
# -----------------------------


@router.get("/search", response_model=List[SweetOut])
async def search_sweets(
    name: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None)
):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if category:
        query["category"] = {"$regex": category, "$options": "i"}
    if min_price is not None or max_price is not None:
        query["price"] = {}
        if min_price is not None:
            query["price"]["$gte"] = min_price
        if max_price is not None:
            query["price"]["$lte"] = max_price

    sweets_cursor = sweets_collection.find(query)
    sweets_raw = await sweets_cursor.to_list(length=100)
    sweets_clean = [
        SweetOut(**{**sweet, "id": str(sweet["_id"])}) for sweet in sweets_raw
    ]
    return sweets_clean

# -----------------------------
# Update a sweet (User Required)
# -----------------------------


@router.put("/{sweet_id}", response_model=SweetOut)
async def update_sweet(sweet_id: str, sweet: SweetUpdate, user=Depends(get_current_user)):
    update_data = {k: v for k, v in sweet.dict().items() if v is not None}
    result = await sweets_collection.update_one(
        {"_id": ObjectId(sweet_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Sweet not found")
    updated = await sweets_collection.find_one({"_id": ObjectId(sweet_id)})
    updated["id"] = str(updated["_id"])
    updated.pop("_id")
    return SweetOut(**updated)

# -----------------------------
# Delete a sweet (Admin Only)
# -----------------------------


@router.delete("/{sweet_id}", dependencies=[Depends(get_current_admin)])
async def delete_sweet(sweet_id: str):
    result = await sweets_collection.delete_one({"_id": ObjectId(sweet_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return {"message": "Sweet deleted"}

# -----------------------------
# Restock a sweet (Admin Only)
# -----------------------------


@router.post("/{id}/restock", dependencies=[Depends(get_current_admin)])
async def restock_sweet(id: str, quantity: RestockRequest):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid sweet ID")

    sweet = await sweets_collection.find_one({"_id": ObjectId(id)})
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    new_quantity = sweet.get("quantity", 0) + quantity.quantity

    result = await sweets_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"quantity": new_quantity}}
    )

    if result.modified_count == 1:
        return {"message": "Sweet restocked successfully", "new_quantity": new_quantity}
    else:
        raise HTTPException(
            status_code=500, detail="Failed to update sweet quantity")
