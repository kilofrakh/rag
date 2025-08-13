# vector repo
from typing import List

class VectorRepository:
    def __init__(self, collection):
        self.collection = collection
    
    def add_documents(self, documents: List[str], embeddings: List[List[float]], ids: List[str]):
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids
        )
    
    def query(self, query_embedding: List[float], top_k: int):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )