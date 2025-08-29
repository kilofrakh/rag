# app/services/chat_service.py
from typing import Dict, Any
from app.repositories.vector_repo import VectorRepository
from app.clients.llm_client import LLMClient
from app.repositories.message_repo import MessageRepository
from app.repositories.chat_repo import ChatRepository
from app.clients.embedding_client import EmbeddingClient
from datetime import datetime
from typing import List

class ChatService:
    def __init__(self, vector_repo: VectorRepository, llm: LLMClient):
        self.vector_repo = vector_repo
        self.llm = llm
        self.message_repo = MessageRepository()
        self.chat_repo = ChatRepository()
        self.embedding_client = EmbeddingClient()

    def start_chat(self, user_id: str) -> str:
        return self.chat_repo.create_chat(user_id)

    def ask(self, chat_id: str, user_id: str, question: str, n_results: int = 5) -> Dict[str, Any]:
        # Create embeddings
        q_embedding = self.embedding_client.encode([question])[0]

        # Query vector DB for context
        query_response = self.vector_repo.query_embedding(
            query_embedding=q_embedding,
            n_results=n_results,
            where={"user_id": user_id}
        )

        docs: List[str] = query_response.get("documents", [])
        metas: List[Dict[str, Any]] = query_response.get("metadatas", [])
        ids: List[Any] = query_response.get("ids", [])

        snippets = []
        for i, text in enumerate(docs):
            md = metas[i] if i < len(metas) else {}
            src = f"[{md.get('filename', 'unknown')}]" if isinstance(md, dict) else ""
            snippets.append(f"{src}\n{text}")

        context = "\n".join(snippets)

        # Ask LLM
        answer = self.llm.generate_answer(question=question, context=context)

        now = datetime.utcnow()

        # persist messages (with chat_id)
        self.message_repo.add_message(user_id=user_id, chat_id=chat_id,
                                      message={"role": "user", "content": question, "created_at": now})
        self.message_repo.add_message(user_id=user_id, chat_id=chat_id,
                                      message={"role": "bot", "content": answer, "created_at": now})

        # persist chat entry
        entry = {"question": question, "answer": answer, "sources": ids, "created_at": now}
        self.chat_repo.add_entry(chat_id=chat_id, entry=entry)

        return {
            "chat_id": chat_id,
            "question": question,
            "answer": answer.strip(),
            "sources": [
                {"id": str(ids[i]) if ids and i < len(ids) else None, "metadata": metas[i] if metas and i < len(metas) else {}}
                for i in range(len(ids))
            ],
        }

    def get_chat(self, chat_id: str):
        return self.chat_repo.get_chat(chat_id)

    def get_user_chats(self, user_id: str):
        return self.chat_repo.get_user_chats(user_id)

    def get_messages(self, chat_id: str):
        return self.message_repo.get_messages_by_chat(chat_id)
