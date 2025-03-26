import os
from typing import List, Optional
from datetime import datetime
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from app.models.chat import ChatMessage, ChatResponse, ChatHistory
from fastapi import HTTPException

class ChatService:
    def __init__(self):
        self.chat_model = ChatAnthropic(
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            model_name="claude-3-opus-20240229",
            max_tokens=1024
        )
        self.conversation_history: List[ChatMessage] = []
        self.system_prompt = "You are a helpful AI assistant."

    async def get_chat_response(self, message: str) -> ChatResponse:
        # Convert conversation history to LangChain message format
        messages = [SystemMessage(content=self.system_prompt)]
        
        for msg in self.conversation_history:
            if msg.role == "user":
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                messages.append(AIMessage(content=msg.content))

        # Add the new message
        messages.append(HumanMessage(content=message))
        
        # Get response from LangChain
        response = await self.chat_model.ainvoke(messages)
        ai_message = response.content

        # Store messages in history
        self.conversation_history.append(
            ChatMessage(content=message, role="user")
        )
        self.conversation_history.append(
            ChatMessage(content=ai_message, role="assistant")
        )

        return ChatResponse(message=ai_message)

    def get_chat_history(self) -> ChatHistory:
        return ChatHistory(messages=self.conversation_history)

    def clear_chat_history(self) -> dict:
        self.conversation_history = []
        return {"message": "Chat history cleared successfully"} 