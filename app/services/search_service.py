import os
from typing import Dict, Any

from app.repositories.vector_repo import VectorRepository
from app.clients.llm_client import LLMClient

class SearchService:
    def __init__(self, vector_repo: VectorRepository, llm: LLMClient):
        self.vector_repo = vector_repo
        self.llm = llm

    def ask(self,user_id: str,question: str,n_results: int = 5) -> Dict[str, Any]:
       
        query_response = self.vector_repo.query_text(
            query_text=question,
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

        context = "\n---\n".join(snippets)

        # el llm beygen el ans
        answer = self.llm.generate_answer(question=question, context=context)

        # elegba elkamla
        return {
            "question": question,
            "answer": answer.strip(),
            "sources": [
                {"id": ids[i], "metadata": metas[i]}
                for i in range(len(ids))
            ]
        }
