from typing import List, Dict, Any, Optional
from bson import ObjectId
from app.clients.mongo_client import get_db
from datetime import datetime

class ChatRepository:
    def __init__(self):
        self.col = get_db()["chats"]

    def create_chat(self, user_id: str) -> str:
        chat_doc = {
            "user_id": user_id,
            "entries": [],
            "created_at": datetime.utcnow()
        }
        result = self.col.insert_one(chat_doc)
        return str(result.inserted_id)

    def add_entry(self, chat_id: str, entry: Dict[str, Any]) -> None:
        self.col.update_one(
            {"_id": ObjectId(chat_id)},
            {"$push": {"entries": entry}}
        )

    def get_chat(self, chat_id: str) -> Optional[Dict[str, Any]]:
        doc = self.col.find_one({"_id": ObjectId(chat_id)})
        if not doc:
            return None

        doc["_id"] = str(doc["_id"])
        if "created_at" in doc and doc["created_at"] is not None:
            doc["created_at"] = doc["created_at"].isoformat()

        entries = doc.get("entries", [])
        for e in entries:
            if "created_at" in e and e["created_at"] is not None:
                e["created_at"] = e["created_at"].isoformat()
        return doc

    def get_user_chats(self, user_id: str) -> List[Dict[str, Any]]:
        chats = list(self.col.find({"user_id": user_id}))
        for c in chats:
            c["_id"] = str(c["_id"])
            if "created_at" in c and c["created_at"] is not None:
                c["created_at"] = c["created_at"].isoformat()
            for e in c.get("entries", []):
                if "created_at" in e and e["created_at"] is not None:
                    e["created_at"] = e["created_at"].isoformat()
        return chats
