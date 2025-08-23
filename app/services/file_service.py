# app/services/upload_service.py
from app.services.pdf_process import PDFProcess
from app.clients.embedding_client import EmbeddingClient
from app.repositories.vector_repo import VectorRepository

class UploadService:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.pdfprocess = PDFProcess()
        self.embedding_client = EmbeddingClient()
        self.vector_repo = VectorRepository()

    async def handle_upload(self, file):
        # Extract text
        text = await self.pdfprocess.extract_text(file)
        chunks = self.pdfprocess.split_text(text)

        # Embed + store with user_id
        embeddings = self.embedding_client.embed_chunks(chunks)
        self.vector_repo.add_documents(
            user_id=self.user_id,
            chunks=chunks,
            embeddings=embeddings,
        )

        return {"status": "success", "chunks_stored": len(chunks)}

    async def delete_document(self, doc_id: str):
        # Delete only documents belonging to this user
        self.vector_repo.delete_document(user_id=self.user_id, doc_id=doc_id)
        return {"status": "deleted", "doc_id": doc_id}
