from typing import Optional, Dict, Any
from bson import ObjectId
from app.core.database import get_db

class UserRepository:
    def __init__(self):
        self.db = get_db()
        self.col = self.db["users"]

    def create_user(self, username: str, password_hash: str) -> str:
        doc = {"username": username, "password_hash": password_hash}
        res = self.col.insert_one(doc)
        return str(res.inserted_id)

    def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        return self.col.find_one({"username": username})

    def get_by_id(self, uid: str) -> Optional[Dict[str, Any]]:
        try:
            return self.col.find_one({"_id": ObjectId(uid)})
        except Exception:
            return None
