from pymongo import MongoClient
from app.core.config import config

MONGO_URI = config.MONGO_URI
MONGO_DB = config.MONGO_DB

_client: MongoClient | None = None
_db = None


def connect():
    global _client, _db
    if _client is None:
        _client = MongoClient(MONGO_URI, uuidRepresentation="standard")
        _db = _client[MONGO_DB]
        print("MongoDB connected.")


def disconnect():
    global _client, _db
    if _client is not None:
        _client.close()
        _client = None
        _db = None
        print("MongoDB disconnected.")


def get_db():
    global _db
    if _db is None:
        connect()
    return _db
