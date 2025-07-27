from fastapi import APIRouter, HTTPException
from ..config.db import db
from ..auth.adminschema import AdminLogin
from ..auth.hasing import verify_password
from ..auth.utils import create_access_token

router = APIRouter(prefix="/auth", tags=["Admin Auth"])


@router.post("/admin/login")
async def admin_login(admin: AdminLogin):
    admin_doc = await db.admin.find_one({"email": admin.email})
    if not admin_doc:
        raise HTTPException(status_code=400, detail="Admin not found")

    if not verify_password(admin.hashed_password, admin_doc["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid password")

    token_data = {
        "sub": str(admin_doc["_id"]),         # for identification
        "username": admin_doc["username"],
        "role": "admin"
    }

    access_token = create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}
