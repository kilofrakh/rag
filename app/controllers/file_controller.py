from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from typing import Optional
from app.core.security import get_current_user_id
from app.services.pdf_process import PDFProcess
from app.repositories.vector_repo import VectorRepository

router = APIRouter(prefix="/docs", tags=["docs"])

pdfproc = PDFProcess()
vec = VectorRepository()

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    pdf_bytes = await file.read()
    text = pdfproc.extract_text(pdf_bytes)
    if not text.strip():
        raise HTTPException(status_code=400, detail="No extractable text in PDF")

    chunks = pdfproc.split_text(text)

    metadatas = [{"user_id": user_id, "filename": file.filename} for _ in chunks]
    ids = vec.add_texts(texts=chunks, metadatas=metadatas)

    return {"message": "uploaded", "chunks": len(chunks), "ids": ids[:3]}  # sample of ids

@router.post("/search")
async def search_docs(
    q: str = Query(..., min_length=1),
    n: int = Query(5, ge=1, le=20),
    user_id: str = Depends(get_current_user_id)
):
    res = vec.query_text(query_text=q, n_results=n, where={"user_id": user_id})
    return res


@router.delete("/delete-all-my-docs")
async def delete_all_my_docs(user_id: str = Depends(get_current_user_id)):
    vec.delete_where(where={"user_id": user_id})
    return {"message": "deleted all your docs"}
