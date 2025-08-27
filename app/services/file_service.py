from app.services.pdf_process import PDFProcess
from app.clients.embedding_client import EmbeddingClient
from app.repositories.vector_repo import VectorRepository
from app.repositories.user_repo import UserRepository
from app.repositories.files_repo import FilesRepository
from bson import ObjectId
from typing import Dict, Any

class UploadService:
    def __init__(self, user_id: str):
        self.user_id = str(user_id)
        self.pdfprocess = PDFProcess()
        self.embedding_client = EmbeddingClient()
        self.vector_repo = VectorRepository()
        self.user_repo = UserRepository()
        self.files_repo = FilesRepository()

    async def handle_upload(self, file):
        self.files_repo.add_file(self.user_id, file.filename)

        pdf_bytes = await file.read()
        text = self.pdfprocess.extract_text(pdf_bytes)

        if not text.strip():
            return {"status": "failed", "reason": "No extractable text in PDF"}

        chunks = self.pdfprocess.split_text(text)
        embeddings = self.embedding_client.encode(chunks)

        metadatas = [
            {"user_id": self.user_id, "filename": file.filename, "chunk_idx": i}
            for i in range(len(chunks))
        ]

        self.vector_repo.add_texts(
            texts=chunks,
            metadatas=metadatas,
            embeddings=embeddings,
        )

        return {"status": "uploaded"}

    async def delete_all_documents(self):
        self.vector_repo.delete_all(where={"user_id": self.user_id})
        self.files_repo.delete_files_by_user(self.user_id)
        return {"status": "all documents deleted"}

    async def delete_document_by_id(self, file_id: str) -> Dict[str, Any]:
        file_doc = self.files_repo.get_file_by_id(file_id)
        if not file_doc:
            return {"status": "file not found", "file_id": file_id}

        where_filter = {
            "$and": [
                {"user_id": self.user_id},
                {"filename": file_doc.get("filename")}
            ]
        }

        self.vector_repo.delete_all(where=where_filter)

        delete_res = self.files_repo.delete_file(file_id)

        return {
            "status": "document deleted" if delete_res["status"] == "deleted" else delete_res["status"],
            "file_id": file_id,
        }

    def list_user_pdfs(self):
        pdfs = self.files_repo.get_files_by_user(self.user_id)
        return pdfs if pdfs else []
