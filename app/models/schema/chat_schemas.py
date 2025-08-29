# app/models/schema/chat_schemas.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class MessageSchema(BaseModel):
    role: str
    content: str
    created_at: datetime

class ChatEntry(BaseModel):
    question: str
    answer: str
    sources: Optional[List[Dict[str, Any]]] = []
    created_at: datetime

class AskRequest(BaseModel):
    question: str
    top_k: int = 5

class AskResponse(BaseModel):
    chat_id: str
    question: str
    answer: str
    sources: List[Dict[str, Any]]

class ChatHistoryResponse(BaseModel):
    chat_id: str
    user_id: str
    created_at: datetime
    entries: List[ChatEntry]
