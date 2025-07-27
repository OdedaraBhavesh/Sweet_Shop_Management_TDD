from pymongo import MongoClient

# Connect to MongoDB (local MongoDB instance)
client = MongoClient("mongodb://localhost:27017")

# Use the 'sweetshop' database
db = client["sweetshop"]

# Access the 'users' collection
users_collection = db["users"]
