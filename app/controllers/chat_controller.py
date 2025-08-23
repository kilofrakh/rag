from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.security import get_current_user_id
from app.services.search_service import SearchService
from app.repositories.vector_repo import VectorRepository
from app.clients.llm_client import LLMClient

chat_router = APIRouter(prefix="/chat", tags=["chat"])

# Initialize once
vector_repo = VectorRepository()
llm_client = LLMClient()
search_service = SearchService(vector_repo, llm_client)

class AskRequest(BaseModel):
    question: str
    top_k: int = 5

class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list

@chat_router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest, user_id: str = Depends(get_current_user_id)):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    result = search_service.ask(user_id=user_id, question=request.question, n_results=request.top_k)
    return result
