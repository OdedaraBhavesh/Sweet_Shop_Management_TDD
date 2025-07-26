from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

MONGO_URL = config("MONGO_URL", default="mongodb://localhost:27017")
MONGO_DB = config("MONGO_DB", default="sweetshop")  # Default fallback

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB]
