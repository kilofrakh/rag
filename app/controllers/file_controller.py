from fastapi import APIRouter, UploadFile, File, HTTPException,Depends
from app.services.file_service import UploadService
from app.deps import get_current_user

upload_router = APIRouter()

#sahef malahash lazma aala haga wahda
upload_service = UploadService()

@upload_router.post("/upload",dependencies=[Depends(get_current_user)])
async def upload_pdf(file: UploadFile = File(...)):
    try:
        return await upload_service.handle_upload(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@upload_router.delete("/delete/{filename}",dependencies=[Depends(get_current_user)])
async def delete_pdf(filename: str):
    try:
        return upload_service.handle_delete(filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
