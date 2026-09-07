from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.api.deps import get_current_user
from app.schemas.chat import ChatRequest, ChatResponse, ConversationResponse
from app.services.chat import handle_chat, get_conversations, get_conversation_messages

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
def ask_question(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    ASK THE AI A QUESTION

    Frontend sends:
        POST /api/chat
        Authorization: Bearer <token>
        {
            "question": "What services does I-Zone offer?"
        }

    Backend returns:
        {
            "answer": "I-Zone offers dedicated development teams...",
            "conversation_id": 1,
            "question": "What services does I-Zone offer?"
        }

    Requires login. Any logged-in user can ask questions.
    """
    return handle_chat(request, current_user, db)


@router.get("/conversations", response_model=list[ConversationResponse])
def list_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    GET ALL CONVERSATIONS FOR CURRENT USER

    Returns a list of all past conversations.
    """
    return get_conversations(current_user, db)


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    GET A SINGLE CONVERSATION WITH ALL MESSAGES

    Returns one conversation and all its messages.
    """
    conversation = get_conversation_messages(conversation_id, current_user, db)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    return conversation
