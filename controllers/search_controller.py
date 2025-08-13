# search controller
from fastapi import APIRouter, UploadFile, File, HTTPException
from models.model_1 import SearchRequest, SearchResult
from models.upload_model import PDFUpload
from services.search_service import SearchService
from services.pdf_process import pdfprocess
from clients.embedding_client import EmbeddingClient
from repositories.vector_repo import VectorRepository

class SearchController:
    def __init__(self, search_service: SearchService):
        self.router = APIRouter()
        self.search_service = search_service
        self._setup_routes()
    
    def _setup_routes(self):
        self.router.post("/search", response_model=SearchResult)(self.search)
        self.router.post("/upload")(self.upload_pdf)
    


    async def search(self, request: SearchRequest):
        results = self.search_service.search(request.query, request.top_k)
        return SearchResult(results=results)
    

    
    async def upload_pdf(file: UploadFile = File(...)):
        try:

            save_path = f"uploads/{file.filename}"
            pdf_path = pdfprocess.upload(file, save_path)
            
            texts = pdfprocess.extract(pdf_path)  
            
            embeddings =EmbeddingClient.encode(texts).tolist()
            ids = [f"{file.filename}_chunk_{i}" for i in range(len(texts))]
            
            VectorRepository.add_documents(
                documents=texts,
                embeddings=embeddings,
                ids=ids,
                metadatas=[{"source": file.filename, "chunk_num": i} for i in range(len(texts))]
            )
            
            return {"message": f"Processed {len(texts)} chunks from {file.filename}"}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))