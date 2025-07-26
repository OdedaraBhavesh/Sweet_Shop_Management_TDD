from fastapi import FastAPI
from app.auth.router import router as auth_router
from .routes.user import router as user_router
from .routes.sweets import router as sweets_router
app = FastAPI(title="Sweet Shop Management")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(sweets_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Sweet Shop!"}
