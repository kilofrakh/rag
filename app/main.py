from fastapi import FastAPI
from app.controllers import file_controller as docs_router  
from app.controllers import auth_controller as auth_router
from app.controllers import chat_controller as chat_router  

app = FastAPI(title="thinkgpt")

app.include_router(auth_router.router)
app.include_router(docs_router.router)
app.include_router(chat_router.chat_router)


@app.get("/")
def read_root():
    return {"message": "shagal ya negm"}