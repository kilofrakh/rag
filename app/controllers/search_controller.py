from fastapi import APIRouter, Depends
from models.schema import SearchRequest, SearchResult
from services.search_service import SearchService
from repositories.vector_repo import VectorRepository   
from clients.embedding_client import EmbeddingClient

search_router = APIRouter()

def get_search_service():
    
    vector_repo = VectorRepository()
    embedder = EmbeddingClient()
    return SearchService(vector_repo, embedder)


@search_router.post("/search", response_model=SearchResult)
async def search(
    request: SearchRequest,
    search_service: SearchService = Depends(get_search_service)):


    results = search_service.search(request.query, request.top_k)
    return SearchResult(results=results)
