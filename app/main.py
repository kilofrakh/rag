from fastapi import FastAPI
from app.controllers.file_controller import file_router 
from app.controllers.chat_controller import chat_router
from app.controllers.auth_controller import auth_router

app = FastAPI(title="thinkgpt", description="developed by kilofrakh")

app.include_router(auth_router)
app.include_router(file_router)
app.include_router(chat_router)


# lifespan 

@app.get("/")
def read_root():
    return {"message": "shagal ya negm"}