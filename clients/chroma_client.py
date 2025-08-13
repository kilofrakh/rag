#chroma client
import chromadb

class ChromaClient:
    def __init__(self):
        self.client = chromadb.EphemeralClient()
    
    def get_collection(self, name: str):
        return self.client.get_or_create_collection(name)