from fastapi import FastAPI
from app.auth.router import router as auth_router

app = FastAPI(title="Sweet Shop Management")

app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Sweet Shop!"}
