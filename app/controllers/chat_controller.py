#controllers / chat
from fastapi import APIRouter, Depends
from app.models.schema import SearchRequest, SearchResult
from app.services.search_service import SearchService
from app.repositories.vector_repo import VectorRepository   
from app.clients.embedding_client import EmbeddingClient
from app.deps import get_current_user


search_router = APIRouter()


# Dependency Injection ya3ni enta mat3melsh create lel objects gowa el route.
# bet3ml function zy get_search_service elle btraga3 el object.
# FastAPI ma3 Depends() by3ml auto call lel function deh we y7ot el object fe el parameter.
# Keda el code byb2a cleaner easy to test we re-usable fe kaza endpoint.

def get_search_service():
    
    vector_repo = VectorRepository()
    embedder = EmbeddingClient()
    return SearchService(vector_repo, embedder)

@search_router.post("/search", response_model=SearchResult)
async def search(
    request: SearchRequest,
    user: dict = Depends(get_current_user)
):
    vector_repo = VectorRepository(user["id"])   # user-specific repo
    embedder = EmbeddingClient()
    search_service = SearchService(vector_repo, embedder)

    results = search_service.search(request.query, request.top_k)
    return SearchResult(results=results)
