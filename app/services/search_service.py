from typing import List

class SearchService:
    def __init__(self, vector_repository, embedding_client):
        self.vector_repo = vector_repository
        self.embedder = embedding_client

    def search(self, query: str, top_k: int) -> List[str]:
        query_embedding = self.embedder.encode(query)

        results = self.vector_repo.query(query_embedding, top_k)
        
        return [doc for docs in results["documents"] for doc in docs]
