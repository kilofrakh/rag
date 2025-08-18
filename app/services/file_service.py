from app.services.pdf_process import PDFProcess
from app.clients.embedding_client import EmbeddingClient
from app.repositories.vector_repo import VectorRepository

class UploadService:
    def __init__(self):
        self.pdfprocess = PDFProcess()
        self.embedding_client = EmbeddingClient()
        self.vector_repo = VectorRepository()

    async def handle_upload(self, file):
        pdf_file = await self.pdfprocess.upload(file)
        texts = self.pdfprocess.extract(pdf_file)

        embeddings = self.embedding_client.encode(texts)
        ids = [f"{file.filename}_chunk_{i}" for i in range(len(texts))]
        

        self.vector_repo.add_documents(
            documents=texts,
            embeddings=embeddings,
            ids=ids,
            metadatas=[{"source": file.filename, "chunk_num": i} for i in range(len(texts))]
        )

        return {"message": f"Processed {file.filename}"}



    # def handle_delete(self, filename: str):
    #     self.vector_repo.delete(where={"source": filename})
    #     return {"message": f"Deleted {filename}"}
