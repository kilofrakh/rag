# app/controllers/file_controller.py
from fastapi import APIRouter, UploadFile, File, Depends
from app.services.file_service import UploadService
from app.deps import get_current_user

upload_router = APIRouter()

@upload_router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    upload_service = UploadService(user_id=str(current_user["_id"]))
    return await upload_service.handle_upload(file)

@upload_router.delete("/delete/{doc_id}")
async def delete_file(
    doc_id: str,
    current_user: dict = Depends(get_current_user),
):
    upload_service = UploadService(user_id=str(current_user["_id"]))
    return await upload_service.delete_document(doc_id)
