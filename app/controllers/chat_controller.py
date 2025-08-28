<<<<<<< Updated upstream
from fastapi import APIRouter, Depends
from app.models.schema import SearchRequest, SearchResult
from app.services.search_service import SearchService
from app.repositories.vector_repo import VectorRepository   
from app.clients.embedding_client import EmbeddingClient
from app.deps import get_current_user
=======
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user_id
from app.services.chat_service import SearchService
from app.repositories.vector_repo import VectorRepository
from app.clients.llm_client import LLMClient
from app.models.schema.chat_schemas import AskRequest, AskResponse
from app.repositories.chat_repo import ChatRepository

chat_router = APIRouter(prefix="/chat", tags=["chat"])
>>>>>>> Stashed changes


search_router = APIRouter()


# Dependency Injection ya3ni enta mat3melsh create lel objects gowa el route.
# bet3ml function zy get_search_service elle btraga3 el object.
# FastAPI ma3 Depends() by3ml auto call lel function deh we y7ot el object fe el parameter.
# Keda el code byb2a cleaner easy to test we re-usable fe kaza endpoint.

def get_search_service():
    
    vector_repo = VectorRepository()
<<<<<<< Updated upstream
    embedder = EmbeddingClient()
    return SearchService(vector_repo, embedder)


@search_router.post("/search", response_model=SearchResult, dependencies=[Depends(get_current_user)])
async def search(
    request: SearchRequest,
    search_service: SearchService = Depends(get_search_service)):


    results = search_service.search(request.query, request.top_k)
    return SearchResult(results=results)
=======
    llm_client = LLMClient()
    return SearchService(vector_repo=vector_repo, llm=llm_client)


@chat_router.post("/ask", response_model=AskResponse)
async def ask(
    request: AskRequest,
    user_id: str = Depends(get_current_user_id),
    chat_service: SearchService = Depends(get_chat_service)
):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # 🔹 Let SearchService handle asking + storing
    result = chat_service.ask(
        user_id=user_id,
        question=request.question,
        n_results=request.top_k
    )

    return AskResponse(**result)


@chat_router.get("/history")
def get_chat_history(user_id: str = Depends(get_current_user_id)):
    chat_repo = ChatRepository()
    chat_history = chat_repo.chat_history(user_id)

    if not chat_history:
        raise HTTPException(status_code=404, detail="No chat history found for user")

    return {"chat_history": chat_history}
>>>>>>> Stashed changes
