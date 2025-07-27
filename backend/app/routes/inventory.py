# app/routers/inventory.py
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from ..models.inventory import InventoryUpdate
from .sweets import sweets_collection
from ..auth.dependencies import get_current_user, admin_required

router = APIRouter(prefix="/api/sweets", tags=["Inventory"])


@router.post("/{sweet_id}/purchase")
async def purchase_sweet(sweet_id: str, data: InventoryUpdate, current_user=Depends(get_current_user)):
    sweet = await sweets_collection.find_one({"_id": ObjectId(sweet_id)})
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    if sweet["quantity"] < data.amount:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    await sweets_collection.update_one(
        {"_id": ObjectId(sweet_id)},
        {"$inc": {"quantity": -data.amount}}
    )

    return {"message": "Purchase successful", "purchased": data.amount}


@router.post("/{sweet_id}/restock")
async def restock_sweet(sweet_id: str, data: InventoryUpdate, current_user=Depends(admin_required)):
    sweet = await sweets_collection.find_one({"_id": ObjectId(sweet_id)})
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    await sweets_collection.update_one(
        {"_id": ObjectId(sweet_id)},
        {"$inc": {"quantity": data.amount}}
    )

    return {"message": "Restocked successfully", "added": data.amount}
