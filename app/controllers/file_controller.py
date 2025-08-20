from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_service import UploadService

upload_router = APIRouter()
upload_service = UploadService()

@upload_router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        return await upload_service.handle_upload(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@upload_router.delete("/delete/{filename}")
async def delete_pdf(filename: str):
    try:
        return upload_service.handle_delete(filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
