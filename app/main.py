from fastapi import FastAPI
from app.controllers.file_controller import file_router 
from app.controllers.chat_controller import chat_router
from app.controllers.auth_controller import auth_router
from app.clients.mongo_client import connect, disconnect
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    connect()
    yield
    disconnect()

app = FastAPI(title="thinkgpt",description="developed by kilofrakh",lifespan=lifespan)

app.include_router(auth_router)
app.include_router(file_router)
app.include_router(chat_router)


@app.get("/")
def read_root():
    return {"message": "shaghal ya negm"}