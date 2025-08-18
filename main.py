from fastapi import FastAPI
from controllers.search_controller import search_router
from controllers.upload_controller import upload_router

app = FastAPI()


app.include_router(search_router)
app.include_router(upload_router)


@app.get("/")
def read_root():
    return {"message": "shaghal"}