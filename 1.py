from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List

embedder = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.create_collection("semantic_search")

docs = [
    "Cats are independent and low-maintenance pets.",
    "Dogs are loyal, energetic, and require regular exercise.",
    "Pizza is made with dough, tomato sauce, and cheese.",
    "Birds like parrots can mimic human speech.",
    "Coffee is a popular beverage made from roasted beans.",
]

collection.add(
    documents=docs,
    embeddings=embedder.encode(docs).tolist(),
    ids=[f"id_{i}" for i in range(len(docs))]
)


app = FastAPI(title="Semantic Search API")

class SearchRequest(BaseModel):
    query: str
    top_k: int = 3

class SearchResult(BaseModel):
    results: List[str]

@app.post("/search", response_model=SearchResult)
def search(request: SearchRequest):
    query_embedding = embedder.encode(request.query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=request.top_k
    )
    return SearchResult(results=results["documents"][0])

@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
