from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.core.security import get_current_user_id
from app.services.file_service import UploadService


file_router = APIRouter(prefix="/docs", tags=["docs"])

def get_upload_service(user_id: str = Depends(get_current_user_id)):
    return UploadService(user_id=user_id)

@file_router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    service: UploadService = Depends(get_upload_service),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    return await service.handle_upload(file)


@file_router.delete("/delete-all-my-docs")
async def delete_all_my_docs(service: UploadService = Depends(get_upload_service)):
    return await service.delete_all_documents()

@file_router.delete("/delete-doc/{file_id}")
async def delete_doc_by_id(
    file_id: str,
    service: UploadService = Depends(get_upload_service)
):
    return await service.delete_document_by_id(file_id)


@file_router.get("/my-pdfs")
def list_my_pdfs(service: UploadService = Depends(get_upload_service)):
    return service.list_user_pdfs()