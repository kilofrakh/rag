from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user_id
from app.services.chat_service import SearchService
from app.repositories.vector_repo import VectorRepository
from app.clients.llm_client import LLMClient
from app.models.schema.chat_schemas import AskRequest, AskResponse

chat_router = APIRouter(prefix="/chat", tags=["chat"])


def get_chat_service():
    vector_repo = VectorRepository()
    llm_client = LLMClient()
    return SearchService(vector_repo=vector_repo, llm=llm_client)





@chat_router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest, user_id: str = Depends(get_current_user_id), chat_service: SearchService = Depends(get_chat_service)):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    result = chat_service.ask(user_id=user_id, question=request.question, n_results=request.top_k)

    return AskResponse(**result)

