import chromadb
import os

class ChromaClient:
    def __init__(self):
        path = os.getenv("CHROMA_PATH", "./chroma_db")
        self.client = chromadb.PersistentClient(path=path)
    
    def get_collection(self, name: str):
        return self.client.get_or_create_collection(name)
    