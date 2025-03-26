from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.models.chat import ChatMessage, ChatResponse, ChatHistory
from app.services.chat_service import ChatService

router = APIRouter()

# Dependency to get the ChatService instance
def get_chat_service():
    return ChatService()

class ChatCompletionRequest(BaseModel):
    message: ChatMessage

@router.post("/completion", response_model=ChatResponse)
async def send_message(
    request: ChatCompletionRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    return await chat_service.get_chat_response(request.message.content)

@router.get("/history", response_model=ChatHistory)
async def get_chat_history(
    chat_service: ChatService = Depends(get_chat_service)
):
    return chat_service.get_chat_history()

@router.delete("/history")
async def clear_chat_history(
    chat_service: ChatService = Depends(get_chat_service)
):
    return chat_service.clear_chat_history() 