from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import time
import uuid

class ChatMessage(BaseModel):
    role: str = "user"
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    model: str
    stream: bool = False  # Default to False for backward compatibility
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000
    top_p: Optional[float] = 1.0
    frequency_penalty: Optional[float] = 0.0
    presence_penalty: Optional[float] = 0.0
    stop: Optional[List[str]] = None

class ChatChoice(BaseModel):
    message: ChatMessage
    index: int
    finish_reason: str
    logprobs: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    id: str = f"chatcmpl-{uuid.uuid4().hex}"
    object: str = "chat.completion"
    created: int = int(time.time())
    model: str
    choices: List[ChatChoice]
    usage: Dict[str, int] = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0
    }

class ChatHistory(BaseModel):
    messages: List[ChatMessage]
    created_at: datetime = datetime.now() 

class ChatDelta(BaseModel):
    role: Optional[str] = None
    content: Optional[str] = None

class ChatStreamChoice(BaseModel):
    delta: ChatDelta
    index: int
    finish_reason: Optional[str] = None

class ChatStreamChunk(BaseModel):
    id: str = f"chatcmpl-{uuid.uuid4().hex}"
    object: str = "chat.completion.chunk"
    created: int = int(time.time())
    model: str
    choices: List[ChatStreamChoice]