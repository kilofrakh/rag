import chromadb
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2") 


documents = [
    "Cats are independent and low-maintenance pets.",
    "Dogs are loyal, energetic, and require regular exercise.",
    "Pizza is made with dough, tomato sauce, and cheese.",
    "Birds like parrots can mimic human speech.",
    "Coffee is a popular beverage made from roasted beans.",
]

embeddings = embedder.encode(documents).tolist()


client = chromadb.Client()
collection = client.create_collection("semantic_search")


collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=[f"id_{i}" for i in range(len(documents))]
)


def semantic_search(query: str, top_k: int = 3):
    query_embedding = embedder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results["documents"][0]


queries = [
    "What are good pets for busy people?",
    "Tell me about Italian food.",
    "What drinks are common in the morning?"
]


for query in queries:
    print(f"\nQuery: '{query}'")
    results = semantic_search(query)
    for doc in results:
        print(f"- {doc}")