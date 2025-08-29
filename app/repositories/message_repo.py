from typing import Dict, Any, List
from bson import ObjectId
from app.clients.mongo_client import get_db
from datetime import datetime

class MessageRepository:
    def __init__(self):
        self.col = get_db()["messages"]

    def add_message(self, user_id: str, chat_id: str, message: Dict[str, Any]) -> str:
        doc = {
            "user_id": user_id,
            "chat_id": ObjectId(chat_id),
            "role": message.get("role"),
            "content": message.get("content"),
            "created_at": message.get("created_at", datetime.utcnow())
        }
        result = self.col.insert_one(doc)
        return str(result.inserted_id)

    def get_messages_by_chat(self, chat_id: str) -> List[Dict[str, Any]]:
        raw = list(self.col.find({"chat_id": ObjectId(chat_id)}).sort("created_at", 1))
        msgs = []
        for m in raw:
            msgs.append({
                "_id": str(m["_id"]),
                "user_id": m["user_id"],
                "chat_id": str(m["chat_id"]),
                "role": m.get("role"),
                "content": m.get("content"),
                "created_at": m.get("created_at").isoformat() if m.get("created_at") else None
            })
        return msgs

    def get_messages_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        raw = list(self.col.find({"user_id": user_id}).sort("created_at", 1))
        msgs = []
        for m in raw:
            msgs.append({
                "_id": str(m["_id"]),
                "user_id": m["user_id"],
                "chat_id": str(m["chat_id"]) if m.get("chat_id") else None,
                "role": m.get("role"),
                "content": m.get("content"),
                "created_at": m.get("created_at").isoformat() if m.get("created_at") else None
            })
        return msgs
