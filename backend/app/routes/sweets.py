# app/routes/sweets.py

from fastapi import APIRouter, HTTPException, Depends
from ..models.sweets import SweetCreate, SweetOut, SweetUpdate
from ..config.db import db
from bson import ObjectId
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/sweets", tags=["Sweets"])

sweets_collection = db["sweets"]


@router.post("/", response_model=SweetOut)
async def create_sweet(sweet: SweetCreate, user=Depends(get_current_user)):
    sweet_dict = sweet.dict()
    result = await sweets_collection.insert_one(sweet_dict)
    sweet_dict["id"] = str(result.inserted_id)
    return sweet_dict


@router.get("/", response_model=list[SweetOut])
async def list_sweets():
    sweets = []
    async for sweet in sweets_collection.find():
        sweet["id"] = str(sweet["_id"])
        sweets.append(SweetOut(**sweet))
    return sweets


@router.get("/{sweet_id}", response_model=SweetOut)
async def get_sweet(sweet_id: str):
    sweet = await sweets_collection.find_one({"_id": ObjectId(sweet_id)})
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    sweet["id"] = str(sweet["_id"])
    return sweet


@router.put("/{sweet_id}", response_model=SweetOut)
async def update_sweet(sweet_id: str, sweet: SweetUpdate, user=Depends(get_current_user)):
    update_data = {k: v for k, v in sweet.dict().items() if v is not None}
    result = await sweets_collection.update_one({"_id": ObjectId(sweet_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Sweet not found")
    updated = await sweets_collection.find_one({"_id": ObjectId(sweet_id)})
    updated["id"] = str(updated["_id"])
    return updated


@router.delete("/{sweet_id}")
async def delete_sweet(sweet_id: str, user=Depends(get_current_user)):
    result = await sweets_collection.delete_one({"_id": ObjectId(sweet_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return {"message": "Sweet deleted"}
