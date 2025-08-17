from fastapi import APIRouter,Depends
from models.schema import SearchRequest, SearchResult
from services.search_service import SearchService

search_router = APIRouter()


@search_router.post("/search", response_model=SearchResult)
async def search(
    request: SearchRequest,
    search_service: SearchService = Depends()
):
    results = search_service.search(request.query, request.top_k)
    return SearchResult(results=results)

