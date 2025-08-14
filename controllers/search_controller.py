from fastapi import APIRouter, UploadFile, File
from models.model_1 import SearchRequest, SearchResult
from models.upload_model import PDFUpload
from services.search_service import SearchService

    def (, search_service: SearchService):
        .search_service = search_service


file_router = APIRouter()


file_router.post("/search", response_model=SearchResult)(self.search)
async def search(self, request: SearchRequest):
    results = self.search_service.search(request.query, request.top_k)
    return SearchResult(results=results)


file_router.post("/upload")(self.upload_pdf)
async def upload_pdf(self, file: UploadFile = File(...)):

    await self.search_service.process_and_store_pdf(file, file.filename)
    return {"message": f"PDF {file.filename} processed successfully"}