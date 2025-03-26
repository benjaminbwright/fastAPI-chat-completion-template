import os
from typing import List, Optional, Generator, AsyncGenerator
from datetime import datetime
from langchain_anthropic import ChatAnthropic
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from app.models.chat import ChatChoice, ChatMessage, ChatResponse, ChatHistory, ChatStreamChunk, ChatStreamChoice, ChatDelta
from fastapi import HTTPException
import uuid
import time
import json

class SSEStreamingCallback(BaseCallbackHandler):
    def __init__(self):
        self.queue: List[str] = []

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.queue.append(token)

class ChatService:
    def __init__(self):
        self.chat_model = ChatAnthropic(
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            model_name="claude-3-opus-20240229",
            max_tokens=1024,
            streaming=True
        )
        self.conversation_history: List[ChatMessage] = []
        self.system_prompt = "You are a helpful AI assistant."
    def _get_llm(self, streaming: bool = False, callback: Optional[BaseCallbackHandler] = None):
        self.chat_model = ChatAnthropic(
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            model_name="claude-3-opus-20240229",
            max_tokens=1024,
            callbacks=[callback] if callback else None,
            streaming=streaming
        )
        return self.chat_model
    
    async def generate_stream_response(self, message: str) -> AsyncGenerator[str, None]:
        """Generate a streaming response for the given message.
        
        Args:
            message: The message to stream
            
        Yields:
            Server-sent event data in the format expected by Open WebUI
        """
        print("Generating stream response")
        callback = SSEStreamingCallback()
        llm = self._get_llm(streaming=True, callback=callback)

        messages = [SystemMessage(content=self.system_prompt)]
        messages.append(HumanMessage(content=message))

        response_id = f"chatcmpl-{uuid.uuid4().hex}"
        created = int(time.time())

        async for chunk in llm.astream(messages):
            if chunk.content:
                stream_chunk = ChatStreamChunk(
                    id=response_id,
                    created=created,
                    model="praxis-1",
                    choices=[
                        ChatStreamChoice(
                            delta=ChatDelta(
                                role="assistant",
                                content=chunk.content
                            ),
                            index=0
                        )
                    ]
                )
                yield f"data: {stream_chunk.json()}\n\n"

        # Send the final message
        final_chunk = ChatStreamChunk(
            id=response_id,
            created=created,
            model="praxis-1",
            choices=[
                ChatStreamChoice(
                    delta=ChatDelta(),
                    index=0,
                    finish_reason="stop"
                )
            ]
        )
        yield f"data: {final_chunk.json()}\n\n"
        yield "data: [DONE]\n\n"

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
        
        # Extract the content and metadata from the response
        ai_message = response.content
        model_name = response.response_metadata.get("model", "unknown")

        # Create message IDs
        user_msg_id = f"msg-{uuid.uuid4().hex}"
        assistant_msg_id = f"msg-{uuid.uuid4().hex}"

        # Create user message
        user_message = ChatMessage(
            id=user_msg_id,
            role="user",
            content=message,
            timestamp=int(time.time()),
            models=[model_name],
            done=True
        )

        # Create assistant message
        assistant_message = ChatMessage(
            id=assistant_msg_id,
            parentId=user_msg_id,
            childrenIds=[],
            role="assistant",
            content=ai_message,  # Use the raw content without additional JSON encoding
            timestamp=int(time.time()),
            models=[model_name],
            model=model_name,
            modelName=model_name,
            modelIdx=0,
            userContext=None,
            done=True
        )

        # Store messages in history
        self.conversation_history.append(user_message)
        self.conversation_history.append(assistant_message)

        # Create and return the response with all required fields
        return ChatResponse(
            id=f"chatcmpl-{uuid.uuid4().hex}",
            object="chat.completion",
            created=int(time.time()),
            model=model_name,
            choices=[
                ChatChoice(
                    message=assistant_message,
                    index=0,
                    finish_reason="stop",
                    logprobs=None
                )
            ],
            usage={
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        )

    def get_chat_history(self) -> ChatHistory:
        return ChatHistory(messages=self.conversation_history)

    def clear_chat_history(self) -> dict:
        self.conversation_history = []
        return {"message": "Chat history cleared successfully"} 
    
    # def get_models(self) -> List[str]:
    #     return [self.chat_model.model_name]