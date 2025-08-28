import uuid
from typing import Dict, Any
from app.repositories.vector_repo import VectorRepository
from app.clients.llm_client import LLMClient
from app.repositories.message_repo import MessageRepository
from app.repositories.chat_repo import ChatRepository
from app.clients.embedding_client import EmbeddingClient
from app.models.message_model import Message
from app.models.chat_model import chat  # fixed class name

class SearchService:
    def __init__(self, vector_repo: VectorRepository, llm: LLMClient):
        self.vector_repo = vector_repo
        self.llm = llm
        self.message_repo = MessageRepository()
        self.chat_repo = ChatRepository()
        self.embedding_client = EmbeddingClient()

    def ask(self, user_id: str, question: str, n_results: int = 5) -> Dict[str, Any]:
        # 1. Embed the question
        question_embedding = self.embedding_client.encode([question])[0]

        # 2. Query vector store
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

        context = "\n\n".join(snippets)

        # 3. Generate answer
        answer = self.llm.generate_answer(question=question, context=context).strip()

        # 4. Create chat_id
        chat_id = str(uuid.uuid4())
        
        
        
        # 5. Store user + bot messages with chat_id
        user_message_id = str(uuid.uuid4())
        self.message_repo.create_message(
            sender="user",
            content=question,
            chat_id=chat_id,
            user_id=user_id,
            message_id=user_message_id
        )

        bot_message_id = str(uuid.uuid4())
        self.message_repo.create_message(
            sender="bot",
            content=answer,
            chat_id=chat_id,
            user_id=user_id,
            message_id=bot_message_id
        )



        # 6. Store chat record
        chat_obj = chat(
            chat_id=chat_id,
            user_id=user_id,
            messages=[
                {"role": "user", "content": question},
                {"role": "bot", "content": answer}
            ]
        )
        self.chat_repo.create_chat(chat_obj)

        # 7. Return response
        return {
            "chat_id": chat_id,
            "question": question,
            "answer": answer,
            "sources": [
                {"id": ids[i], "metadata": metas[i]}
                for i in range(len(ids))
            ]
        }
