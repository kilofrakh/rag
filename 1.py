import chromadb
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2") 
client = chromadb.Client()

docs = [
    "Cats are independent and low-maintenance pets.",
    "Dogs are loyal, energetic, and require regular exercise.",
    "Pizza is made with dough, tomato sauce, and cheese.",
    "Birds like parrots can mimic human speech.",
    "Coffee is a popular beverage made from roasted beans.",
]


client.create_collection("search").add(
    documents=docs,
    embeddings=embedder.encode(docs).tolist(),
    ids=[f"id_{i}" for i in range(len(docs))]
)


def search(query, n=3):
    return client.get_collection("search").query(
        query_embeddings=[embedder.encode(query).tolist()],
        n_results=n
    )["documents"][0]


for q in [
    "What are good pets for busy people?",
    "Tell me about Italian food.",
    "What drinks are common in the morning?"
]:
    print(f"\nQ: {q}")
    for result in search(q):
        print(f"- {result}")