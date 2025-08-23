from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import file_controller as docs_router  # or app.routers.docs_router if you placed it there
from app.controllers import auth_controller as auth_router
from app.controllers import chat_controller as chat_router  # new import

app = FastAPI(title="thinkgpt")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(docs_router.router)
app.include_router(chat_router.chat_router)

# (include any other routers you already have)

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG with Per-User Chroma API"}