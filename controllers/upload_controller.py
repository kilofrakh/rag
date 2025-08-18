from fastapi import APIRouter, UploadFile, File, HTTPException
from services.pdf_process import PDFProcess
from clients.embedding_client import EmbeddingClient
from repositories.vector_repo import VectorRepository
import os

upload_router = APIRouter()

pdfprocess = PDFProcess
embedding_client = EmbeddingClient
vector_repo = VectorRepository

@upload_router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        os.makedirs("uploads", exist_ok=True)
        
        save_path = f"uploads/{file.filename}"
        pdf_path = await pdfprocess.upload(file, save_path)
        
        texts = pdfprocess.extract(pdf_path)  
        
        embeddings = embedding_client.encode(texts).tolist()
        ids = [f"{file.filename}_chunk_{i}" for i in range(len(texts))]
        
        vector_repo.add_documents(
            documents=texts,
            embeddings=embeddings,
            ids=ids,
            metadatas=[{"source": file.filename, "chunk_num": i} for i in range(len(texts))]
        )
        
        return {"message": f"Processed {len(texts)} chunks from {file.filename}"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))