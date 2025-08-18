from fastapi import FastAPI, UploadFile, File
from clients.chroma_client import ChromaClient
from clients.embedding_client import EmbeddingClient
from repositories.vector_repo import VectorRepository
from services.search_service import SearchService
from controllers.search_controller import search_router , search
from controllers.upload_controller import upload_router , upload_pdf



app = FastAPI(title="Semantic Search API")

app.include_router(search_router)
app.include_router(upload_router)


chroma_client = ChromaClient()
embedding_client = EmbeddingClient()


collection = chroma_client.get_collection(name="pdf_documents")
vector_repository = VectorRepository(collection=collection)


search_service = SearchService(
    vector_repository=vector_repository,
    embedding_client=embedding_client
)





