from typing import List
from app.clients.mongo_client import get_db
from app.models.chat_model import chat

class ChatRepository:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db['chats']
    
    class ChatRepository:
        def create_chat(self, user_id: str, chat: chat):
            chat_dict = chat.model_dump()
            self.col.insert_one(chat_dict)
            return chat_dict


    def chat_history(self, user_id: str) -> List[chat]:
        chats = self.collection.find({"user_id": user_id})
        return [chat(**c) for c in chats]
