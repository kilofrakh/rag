import os
import uuid
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
from app.clients.chroma_client import ChromaClient
from app.clients.embedding_client import EmbeddingClient

load_dotenv()

class VectorRepository:
    def __init__(self, collection_name: str = "pdf_chunks"):
        self.client = ChromaClient()
        self.collection = self.client.get_collection(name=collection_name)
        self.embedding_client = EmbeddingClient()

    def add_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        embeddings: Optional[List[List[float]]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in texts]

        if embeddings is None:
            embeddings = self.embedding_client.encode(texts)

        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings,
        )
        return ids

    def query_text(
        self,
        query_text: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        query_embedding = self.embedding_client.encode([query_text])[0]
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
        )

    def query_embedding(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
        )

    def delete_all(self, where: Dict[str, Any]) -> None:
        self.collection.delete(where=where)
