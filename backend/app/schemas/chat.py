from pydantic import BaseModel
from datetime import datetime


class ChatRequest(BaseModel):
    """
    What the frontend sends when a user asks a question.

    Example JSON:
    {
        "question": "What services does I-Zone offer?"
    }
    """
    question: str


class ChatResponse(BaseModel):
    """
    What the backend returns after generating an answer.

    Example JSON:
    {
        "answer": "I-Zone offers dedicated development teams...",
        "conversation_id": 1,
        "question": "What services does I-Zone offer?"
    }
    """
    answer: str
    conversation_id: int
    question: str


class MessageResponse(BaseModel):
    """A single message in a conversation."""
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    """A conversation with all its messages."""
    id: int
    title: str
    created_at: datetime
    messages: list[MessageResponse] = []

    class Config:
        from_attributes = True
