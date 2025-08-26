from pymongo import MongoClient
from app.core.config import config


MONGO_URI = config.MONGO_URI
MONGO_DB = config.MONGO_DB

_client = MongoClient(MONGO_URI, uuidRepresentation="standard")
_db = _client[MONGO_DB]

def get_db():
    return _db


# connect w disconnect 