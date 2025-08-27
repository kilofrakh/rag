from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user_id
from app.services.chat_service import SearchService
from app.repositories.vector_repo import VectorRepository
from app.clients.llm_client import LLMClient
from app.models.schema.chat_schemas import AskRequest, AskResponse
from app.repositories.user_repo import UserRepository
from app.repositories.chat_repo import ChatRepository
from app.repositories.message_repo import MessageRepository
from app.clients.embedding_client import EmbeddingClient

chat_router = APIRouter(prefix="/chat", tags=["chat"])


def get_chat_service():
    vector_repo = VectorRepository()
    llm_client = LLMClient()
    chat_repo = ChatRepository()
    message_repo = MessageRepository()
    embedding_client = EmbeddingClient()

    return SearchService(vector_repo=vector_repo, llm=llm_client)



@chat_router.post("/ask", response_model=AskResponse)
async def ask(
    request: AskRequest,
    user_id: str = Depends(get_current_user_id),
    chat_service: SearchService = Depends(get_chat_service)
):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    result = chat_service.ask(user_id=user_id, question=request.question, n_results=request.top_k)

    chat_repo = ChatRepository()
    message_repo = MessageRepository()
    chat_history = chat_repo.add_message(user_id, {"question": request.question, "answer": result["answer"], "sources": result["sources"]
    })
    message_repo.add_message(user_id, {"role": "user", "content": request.question})
    message_repo.add_message(user_id, {"role": "bot", "content": result["answer"]})





    return AskResponse(**result)

@chat_router.get("/history")
def get_chat_history(user_id: str = Depends(get_current_user_id)):
    chat_repo = ChatRepository()
    chat_history = chat_repo.get_history(user_id)
    if chat_history is None:
        raise HTTPException(status_code=404, detail="No chat history found for user")   
    


    return {"chat_history": chat_history}

