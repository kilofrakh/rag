# app/controllers/chat_controller.py
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user_id
from app.services.chat_service import ChatService
from app.repositories.vector_repo import VectorRepository
from app.clients.llm_client import LLMClient
from app.models.schema.chat_schemas import AskRequest, AskResponse, ChatHistoryResponse
from typing import Any

chat_router = APIRouter(prefix="/chat", tags=["chat"])

def get_chat_service() -> ChatService:
    # create service with your real VectorRepo/LLM clients in production
    return ChatService(vector_repo=VectorRepository(), llm=LLMClient())

@chat_router.post("/start")
def start_chat(user_id: str = Depends(get_current_user_id), chat_service: ChatService = Depends(get_chat_service)):
    chat_id = chat_service.start_chat(user_id)
    return {"chat_id": chat_id}

@chat_router.post("/{chat_id}/ask", response_model=AskResponse)
async def ask(
    chat_id: str,
    request: AskRequest,
    user_id: str = Depends(get_current_user_id),
    chat_service: ChatService = Depends(get_chat_service)
):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    result = chat_service.ask(chat_id=chat_id, user_id=user_id, question=request.question, n_results=request.top_k)
    return AskResponse(**result)

@chat_router.get("/{chat_id}")
def get_chat(chat_id: str, chat_service: ChatService = Depends(get_chat_service)):
    chat = chat_service.get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    # chat already serialized in repo (created_at iso strings)
    return chat

@chat_router.get("/{chat_id}/messages")
def get_chat_messages(chat_id: str, chat_service: ChatService = Depends(get_chat_service)):
    messages = chat_service.get_messages(chat_id)
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this chat")
    return {"chat_id": chat_id, "messages": messages}

@chat_router.get("/user/chats")
def get_user_chats(user_id: str = Depends(get_current_user_id), chat_service: ChatService = Depends(get_chat_service)):
    chats = chat_service.get_user_chats(user_id)
    return {"user_id": user_id, "chats": chats}
