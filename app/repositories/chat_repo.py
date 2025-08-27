from typing import List, Dict, Any, Optional
from bson import ObjectId
from app.clients.mongo_client import get_db

class ChatRepository:
    def __init__(self):
        self.db = get_db()
        self.col = self.db["chats"]

    def add_message(self, user_id: str, message: Dict[str, Any]) -> None:
        self.col.update_one(
            {"user_id": user_id},
            {"$push": {"messages": message}},
            upsert=True
        )

    def get_history(self, user_id: str) -> List[Dict[str, Any]]:
        doc = self.col.find_one({"user_id": user_id})
        return doc.get("messages", []) if doc else []

