from typing import List, Dict, Any, Optional
from bson import ObjectId
from app.clients.mongo_client import get_db

class MessageRepository:
    def __init__(self):
        self.db = get_db()
        self.col = self.db["messages"]

    def add_message(self, user_id: str, message: Dict[str, Any]) -> str:
        doc = {
            "user_id": user_id,
            **message
        }
        result = self.col.insert_one(doc)
        return str(result.inserted_id)
