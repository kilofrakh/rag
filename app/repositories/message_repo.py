from app.clients.mongo_client import get_db
from app.models.message_model import Message

class MessageRepository:
    def __init__(self):
        self.db = get_db()
        self.col = self.db["messages"]

    def create_message(self, sender: str, content: str, chat_id: str, user_id: str, message_id: str) -> Message:
        new_message = Message(
            sender=sender,
            content=content,
            chat_id=chat_id,
            user_id=user_id,
            message_id=message_id
        )

        self.col.insert_one(new_message.model_dump(by_alias=True))
        return new_message
