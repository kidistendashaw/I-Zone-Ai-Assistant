from sqlalchemy.orm import Session
from app.db.models import Conversation, Message, User
from app.rag.embedder import embed_text
from app.rag.vector_store import search_similar_chunks
from app.rag.generator import generate_answer
from app.schemas.chat import ChatRequest, ChatResponse


def handle_chat(request: ChatRequest, current_user: User, db: Session) -> ChatResponse:
    """
    The full chat pipeline:

    1. Convert question to vector
    2. Search ChromaDB for relevant chunks
    3. Generate answer using Ollama
    4. Save conversation and messages to PostgreSQL
    5. Return the answer

    Every question creates or continues a conversation.
    """

    # Step 1 — Convert question to vector using Ollama embedding model
    question_embedding = embed_text(request.question)

    # Step 2 — Find relevant chunks from ChromaDB
    relevant_chunks = search_similar_chunks(question_embedding, n_results=5)

    # Step 3 — Generate answer using Ollama LLM
    answer = generate_answer(request.question, relevant_chunks)

    # Step 4 — Save to PostgreSQL
    # Create a new conversation for each question (can be improved later)
    conversation = Conversation(
        user_id=current_user.id,
        title=request.question[:50]  # use first 50 chars of question as title
    )
    db.add(conversation)
    db.flush()  # get the conversation id without committing yet

    # Save the user's question
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.question
    )
    db.add(user_message)

    # Save the AI's answer
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=answer
    )
    db.add(assistant_message)
    db.commit()

    # Step 5 — Return the answer
    return ChatResponse(
        answer=answer,
        conversation_id=conversation.id,
        question=request.question
    )


def get_conversations(current_user: User, db: Session):
    """Returns all conversations for the current user."""
    return (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .order_by(Conversation.created_at.desc())
        .all()
    )


def get_conversation_messages(
    conversation_id: int,
    current_user: User,
    db: Session
):
    """Returns a single conversation with all its messages."""
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
        .first()
    )
    return conversation
