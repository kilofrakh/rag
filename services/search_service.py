
from typing import List
import os
from services.pdf_process import pdfprocess

class SearchService:
    def __init__(self, vector_repository, embedding_client, upload_dir="uploads"):
        self.vector_repo = vector_repository
        self.embedder = embedding_client
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    async def process_and_store_pdf(self, file, filename: str) -> bool:
        
        
        save_path = os.path.join(self.upload_dir, filename)
        pdf_path = pdfprocess.upload(file, save_path)
        
        
        texts = pdfprocess.extract(pdf_path)
        
        
        embeddings = self.embedder.encode(texts)
        ids = [f"{filename}_page_{i}" for i in range(len(texts))]
        
        self.vector_repo.add_documents(
            documents=texts,
            embeddings=embeddings,
            ids=ids
        )
        return True

    def search(self, query: str, top_k: int) -> List[str]:
        query_embedding = self.embedder.encode(query)
        results = self.vector_repo.query(query_embedding, top_k)
        return results["documents"][0]  