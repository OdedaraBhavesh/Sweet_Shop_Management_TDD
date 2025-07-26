from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
db = client.sweetshop
sweets_collection = db.get_collection("sweets")
