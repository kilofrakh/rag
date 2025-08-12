# controllers/search_controller.py
from fastapi import APIRouter, UploadFile, File
from models.model_1 import SearchRequest, SearchResult
from models.upload_model import PDFUpload
from services.search_service import SearchService

class SearchController:
    def __init__(self, search_service: SearchService):
        self.router = APIRouter()
        self.search_service = search_service
        self._setup_routes()
    
    def _setup_routes(self):
        self.router.post("/search", response_model=SearchResult)(self.search)
        self.router.post("/upload")(self.upload_pdf)
    
    async def search(self, request: SearchRequest):
        return self.search_service.search(request.query, request.top_k)
    


    async def upload_pdf(self, file: UploadFile = File(...)):
        
        await self.search_service.process_and_store_pdf(file, file.filename)
        return {"message": f"PDF {file.filename} processed successfully"}