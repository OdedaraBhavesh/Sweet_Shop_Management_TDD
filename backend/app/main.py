from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi import FastAPI
from app.auth.router import router as auth_router
from .routes.user import router as user_router
from .routes.sweets import router as sweets_router
from .routes.admin import router as admin_router
from .routes.carts import router as cart_router
from fastapi.middleware.cors import CORSMiddleware
from app.models.incomingregister import RegisterUser
from app.models.collection import users_collection
from app.models.incomingLogin import LoginUser


app = FastAPI(title="Sweet Shop Management")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(sweets_router)
app.include_router(admin_router)
app.include_router(cart_router)


origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Sweet Shop!"}


@app.post("/register")
async def register_user(user: RegisterUser):
    # Check if user already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")

    # Insert into database
    users_collection.insert_one(user.dict())
    return {"message": "User registered successfully"}


@app.post("/login")
async def login_user(user: LoginUser):
    # Check if user with email exists
    existing_user = users_collection.find_one({"email": user.email})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if password matches
    if existing_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"message": "Login successful"}
