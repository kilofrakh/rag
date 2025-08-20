import chromadb

class VectorRepository:
    def __init__(self, collection_name: str = "default"):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.file_index = {}  

    def add_documents(self, documents, embeddings, ids, metadatas=None, filename: str = None):
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas,
        )

        if filename:
            if filename not in self.file_index:
                self.file_index[filename] = []
                
            self.file_index[filename].extend(ids)


    def query(self, query_embedding, top_k=5):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )
        return results

    def delete_file(self, filename: str):

        if filename not in self.file_index:
            return {"message": f"No  {filename}"}

        ids_delete = self.file_index[filename]
        self.collection.delete(ids=ids_delete)

        del self.file_index[filename]

        return {"message": f"Deleted {filename}"}
