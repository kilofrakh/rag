from fastapi import APIRouter, UploadFile, File, Depends
from services.search_service import SearchService

upload_router = APIRouter()

@upload_router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    search_service: SearchService = Depends()
):
    await search_service.process_and_store_pdf(file, file.filename)
    return {"message": f"PDF {file.filename} processed successfully"}
