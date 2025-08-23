# app/repositories/vector_repo.py
class VectorRepository:
    def __init__(self):
        from chromadb import Client
        self.client = Client()
        self.collection = self.client.get_or_create_collection("documents")

    def add_documents(self, user_id: str, chunks, embeddings):
        ids = [f"{user_id}_{i}" for i in range(len(chunks))]
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=[{"user_id": user_id} for _ in chunks],
            ids=ids,
        )

    def delete_document(self, user_id: str, doc_id: str):
        # Ensure only this user’s docs are deleted
        self.collection.delete(where={"user_id": user_id, "doc_id": doc_id})
