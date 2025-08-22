# core / database
import os
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "ragdb")

_client = MongoClient(MONGO_URI, uuidRepresentation="standard")
_db = _client[MONGO_DB]

def get_db():
    return _db

# optional: ensure indexes once at import time
_users = _db["users"]
_users.create_index([("username", ASCENDING)], unique=True)
