from fastapi import FastAPI
from app.controllers.chat_controller import search_router
from app.controllers.file_controller import upload_router

app = FastAPI()


app.include_router(search_router)
app.include_router(upload_router)


@app.get("/")
def read_root():
    return {"message": "shaghal"}