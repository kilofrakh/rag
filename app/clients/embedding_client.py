from sentence_transformers import SentenceTransformer

class EmbeddingClient:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.embedder = SentenceTransformer(model_name)
    
    def encode(self, text: str):
        return self.embedder.encode(text).tolist()