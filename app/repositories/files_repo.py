from app.clients.mongo_client import get_db
from typing import List, Dict, Any, Optional
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()


def serialize_doc(doc: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    return doc


class FilesRepository:
    def __init__(self):
        self.db = get_db()
        self.col = self.db["files"]

    def add_file(self, user_id: str, filename: str) -> str:
        doc = {
            "user_id": user_id,
            "filename": filename,
        }
        res = self.col.insert_one(doc)
        return str(res.inserted_id)

    def get_files_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        docs = list(self.col.find({"user_id": user_id}))
        return [serialize_doc(d) for d in docs]

    def get_file_by_id(self, file_id: str) -> Optional[Dict[str, Any]]:
        try:
            doc = self.col.find_one({"_id": ObjectId(file_id)})
            return serialize_doc(doc)
        except Exception:
   
            return None
    
        
    def delete_file(self, file_id: str) -> Dict[str, Any]:
        try:
            obj_id = ObjectId(file_id)
        except Exception:
            return {"status": "invalid file id", "file_id": file_id}

        res = self.col.delete_one({"_id": obj_id})
        return {
            "status": "deleted" if res.deleted_count > 0 else "file not found",
            "file_id": file_id,
        }


    def delete_files_by_user(self, user_id: str) -> Dict[str, Any]:
        res = self.col.delete_many({"user_id": user_id})
        return {"status": "deleted", "count": res.deleted_count}
