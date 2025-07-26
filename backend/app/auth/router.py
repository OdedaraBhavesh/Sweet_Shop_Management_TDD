from fastapi import APIRouter, HTTPException, status
from .schema import UserCreate, Token, UserOut
from ..config.db import db
from .hasing import hash_password, verify_password
from .utils import create_access_token
from bson import ObjectId

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = hash_password(user.password)
    user_dict = {"email": user.email, "password": hashed_pwd}
    result = await db.users.insert_one(user_dict)

    # Return only email, not password
    return {"id": str(result.inserted_id), "email": user.email}


@router.post("/login", response_model=Token)
async def login(user: UserCreate):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(db_user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}
