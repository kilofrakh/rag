import chromadb

class VectorRepository:
    def __init__(self, collection_name: str = "default"):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_documents(self, documents, embeddings, ids, metadatas=None):
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas,
        )

    def query(self, query_embedding, top_k=5):
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )
        return results

# # 
#     def delete(self, source: str):
#         return self.collection.delete(where={"source": source})