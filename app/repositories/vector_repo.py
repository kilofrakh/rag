import os
import uuid
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class VectorRepository:
    def __init__(self, collection_name: str = "pdf_chunks"):
        import chromadb
        from chromadb.config import Settings

        path = os.getenv("CHROMA_PATH", "./chroma_db")
        self.client = chromadb.PersistentClient(path=path, settings=Settings())
        self.collection = self.client.get_or_create_collection(collection_name)

    def add_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in texts]
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        return ids

    def query_text(
        self,
        query_text: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where
        )

    def delete_where(self, where: Dict[str, Any]) -> None:
        self.collection.delete(where=where)
