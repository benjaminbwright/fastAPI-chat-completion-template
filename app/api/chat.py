from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.models.chat import ChatRequest, ChatMessage, ChatResponse, ChatHistory
from app.services.chat_service import ChatService
from typing import Dict, List, Optional
import uuid
import time

router = APIRouter()

# Dependency to get the ChatService instance
def get_chat_service():
    return ChatService()

@router.post("/chat/completions")
async def send_message(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Handle chat completion requests with support for both streaming and non-streaming responses."""
    if request.stream:
        return StreamingResponse(
            chat_service.generate_stream_response(request.messages[-1].content),
            media_type="text/event-stream"
        )
    else:
        return await chat_service.get_chat_response(request.messages[0].content)

@router.get("/chat/history", response_model=ChatHistory)
async def get_chat_history(
    chat_service: ChatService = Depends(get_chat_service)
):
    return chat_service.get_chat_history()

@router.delete("/chat/history")
async def clear_chat_history(
    chat_service: ChatService = Depends(get_chat_service)
):
    return chat_service.clear_chat_history()

@router.get("/models")
async def get_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "praxis-1",
                "object": "model",
                "created": 0,
                "owned_by": "you"
            }
        ]
    }

# Open WebUI format endpoint
@router.get("/webui/history")
async def get_webui_history(
    chat_service: ChatService = Depends(get_chat_service)
):
    history = chat_service.get_chat_history()
    
    # Convert to Open WebUI format
    messages_dict = {}
    messages_list = []
    
    for msg in history.messages:
        message_dict = {
            "id": msg.id,
            "parentId": msg.parentId,
            "childrenIds": msg.childrenIds,
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.timestamp,
            "models": msg.models,
            "model": msg.model,
            "modelName": msg.modelName,
            "modelIdx": msg.modelIdx,
            "userContext": msg.userContext,
            "done": msg.done
        }
        messages_dict[msg.id] = message_dict
        messages_list.append(message_dict)
    
    return {
        "id": str(uuid.uuid4()),
        "user_id": str(uuid.uuid4()),
        "title": "Chat History",
        "chat": {
            "id": "",
            "title": "Chat History",
            "models": [msg.model for msg in history.messages if msg.model],
            "params": {},
            "history": {
                "messages": messages_dict,
                "currentId": messages_list[-1]["id"] if messages_list else None
            },
            "messages": messages_list,
            "tags": [],
            "timestamp": int(time.time() * 1000),
            "files": []
        },
        "updated_at": int(time.time()),
        "created_at": int(time.time()),
        "share_id": None,
        "archived": False,
        "pinned": False,
        "meta": {
            "tags": []
        },
        "folder_id": None
    }