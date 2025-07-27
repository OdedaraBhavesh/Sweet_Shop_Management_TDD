from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from config.db import db
from app.auth.dependencies import get_current_user
from app.auth.cart_schema import CartItem, CartOutItem, UpdateCartQuantity
from typing import List

router = APIRouter(prefix="/carts", tags=["Carts"])
carts_collection = db["carts"]

# Add item to cart


@router.post("/add", response_model=CartOutItem)
async def add_to_cart(item: CartItem, user=Depends(get_current_user)):
    if not ObjectId.is_valid(item.sweet_id):
        raise HTTPException(status_code=400, detail="Invalid sweet ID")

    existing = await carts_collection.find_one({
        "user_id": user["id"],
        "sweet_id": item.sweet_id
    })

    if existing:
        new_quantity = existing["quantity"] + item.quantity
        await carts_collection.update_one(
            {"_id": existing["_id"]},
            {"$set": {"quantity": new_quantity}}
        )
        return {"sweet_id": item.sweet_id, "quantity": new_quantity}

    await carts_collection.insert_one({
        "user_id": user["id"],
        "sweet_id": item.sweet_id,
        "quantity": item.quantity
    })
    return {"sweet_id": item.sweet_id, "quantity": item.quantity}


# Get all items in the user's cart
@router.get("/", response_model=List[CartOutItem])
async def get_cart(user=Depends(get_current_user)):
    items = []
    async for item in carts_collection.find({"user_id": user["id"]}):
        items.append({
            "sweet_id": item["sweet_id"],
            "quantity": item["quantity"]
        })
    return items


# Update quantity
@router.put("/{sweet_id}", response_model=CartOutItem)
async def update_cart_quantity(sweet_id: str, update: UpdateCartQuantity, user=Depends(get_current_user)):
    if not ObjectId.is_valid(sweet_id):
        raise HTTPException(status_code=400, detail="Invalid sweet ID")

    result = await carts_collection.update_one(
        {"user_id": user["id"], "sweet_id": sweet_id},
        {"$set": {"quantity": update.quantity}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    return {"sweet_id": sweet_id, "quantity": update.quantity}


# Remove item
@router.delete("/{sweet_id}")
async def remove_from_cart(sweet_id: str, user=Depends(get_current_user)):
    if not ObjectId.is_valid(sweet_id):
        raise HTTPException(status_code=400, detail="Invalid sweet ID")

    result = await carts_collection.delete_one({
        "user_id": user["id"],
        "sweet_id": sweet_id
    })

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    return {"message": "Item removed from cart successfully"}

# Add to cart
