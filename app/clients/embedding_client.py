import cohere
from typing import List
from app.core.config import config

EMBEDD_KEY = config.EMBEDD_KEY

class EmbeddingClient:
    def __init__(self, api_key: str = EMBEDD_KEY, model_name: str = "embed-english-v3.0"):
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("Cohere API key not found. Please set COHERE_API_KEY env variable.")
        
        self.client = cohere.Client(self.api_key)
        self.model_name = model_name

    def encode(self, text: str) -> List[float]:
        response = self.client.embed(
            texts=[text],
            model=self.model_name
        )
        return response.embeddings[0]
