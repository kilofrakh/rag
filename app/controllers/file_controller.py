from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.core.security import get_current_user_id
from app.services.pdf_process import PDFProcess
from app.repositories.vector_repo import VectorRepository


file_router = APIRouter(prefix="/docs", tags=["docs"])

def get_pdf_service():
    pdfproc = PDFProcess()
    return pdfproc

def get_vec_service():
    vector_repo = VectorRepository()
    return vector_repo

@file_router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
    pdfproc: get_pdf_service = Depends(get_pdf_service),
    vector_repo: VectorRepository = Depends(get_vec_service)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    pdf_bytes = await file.read()
    
    text = pdfproc.extract_text(pdf_bytes)
    if not text.strip():
        raise HTTPException(status_code=400, detail="No extractable text in PDF")

    chunks = pdfproc.split_text(text)

    metadatas = [{"user_id": user_id, "filename": file.filename} for _ in chunks]
    vector_repo.add_texts(texts=chunks, metadatas=metadatas)

    return {"message": "uploaded"}  


@file_router.delete("/delete-all-my-docs")
async def delete_all_my_docs(user_id: str = Depends(get_current_user_id),vector_repo: VectorRepository = Depends(get_vec_service)):
    
    vector_repo.delete_all(where={"user_id": user_id})

    return {"message": "deleted all your docs"}
