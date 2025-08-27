from typing import Dict, Any
from app.repositories.vector_repo import VectorRepository
from app.clients.llm_client import LLMClient
from app.repositories.message_repo import MessageRepository
from app.repositories.chat_repo import ChatRepository
from app.clients.embedding_client import EmbeddingClient


class SearchService:
    def __init__(self, vector_repo: VectorRepository, llm: LLMClient):
        self.vector_repo = vector_repo
        self.llm = llm
        self.message_repo = MessageRepository()
        self.chat_repo = ChatRepository()
        self.embedding_client = EmbeddingClient()

    def ask(self, user_id: str, question: str, n_results: int = 5) -> Dict[str, Any]:
        
        question_embedding = self.embedding_client.encode([question])[0]

        
        query_response = self.vector_repo.query_embedding(
            query_embedding=question_embedding,
            n_results=n_results,
            where={"user_id": user_id}
        )



        docs = query_response.get("documents", [])
        metas = query_response.get("metadatas", [])
        ids = query_response.get("ids", [])

        snippets = []
        for i, text in enumerate(docs):
            md = metas[i] if i < len(metas) else {}
            src = f"[{md.get('filename', 'unknown')}]" if isinstance(md, dict) else ""
            snippets.append(f"{src}\n{text}")

        context = "".join(snippets)

        answer = self.llm.generate_answer(question=question, context=context)

        self.message_repo.add_message(user_id, {"role": "user", "content": question})
        self.message_repo.add_message(user_id, {"role": "bot", "content": answer})
        self.chat_repo.add_message(user_id, {"question": question, "answer": answer, "sources": ids})

        return {
            "question": question,
            "answer": answer.strip(),
            "sources": [
                {"id": ids[i], "metadata": metas[i]}
                for i in range(len(ids))
            ],
        }
