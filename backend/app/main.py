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


app = FastAPI(title="The Sweet Spot")

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


@app.post("/cart")
async def add_to_cart(item: dict):
    cart_collection.insert_one(item)
    return {"message": "Item added to cart"}

# Get cart items


@app.get("/cart")
async def get_cart():
    items = list(cart_collection.find({}, {'_id': 0}))  # exclude _id if needed
    return items

# Remove from cart


@app.delete("/cart/{item_id}")
async def remove_from_cart(item_id: str):
    cart_collection.delete_one({"_id": ObjectId(item_id)})
    return {"message": "Item removed from cart"}


@app.post("/cart/add")
async def add_to_cart(request: Request):
    data = await request.json()
    sweet_id = data.get("sweet_id")
    quantity = data.get("quantity", 1)

    user_id = request.session.get("user_id")
    if not user_id:
        return JSONResponse({"message": "Not logged in"}, status_code=401)

    carts.insert_one({
        "user_id": user_id,
        "sweet_id": sweet_id,
        "quantity": quantity
    })
    return {"message": "Added to cart"}


@app.delete("/cart/remove")
async def remove_from_cart(request: Request):
    data = await request.json()
    sweet_id = data.get("sweet_id")

    user_id = request.session.get("user_id")
    if not user_id:
        return JSONResponse({"message": "Not logged in"}, status_code=401)

    carts.delete_one({
        "user_id": user_id,
        "sweet_id": sweet_id
    })
    return {"message": "Removed from cart"}
