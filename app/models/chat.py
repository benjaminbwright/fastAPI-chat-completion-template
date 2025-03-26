from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    content: str
    role: str = "user"
    created_at: datetime = datetime.now()

class ChatResponse(BaseModel):
    message: str
    created_at: datetime = datetime.now()

class ChatHistory(BaseModel):
    messages: List[ChatMessage]
    created_at: datetime = datetime.now() 