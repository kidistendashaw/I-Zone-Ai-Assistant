import os
import shutil
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import Document, User

# This is the folder where uploaded files will be saved on disk.
# It will be created automatically if it doesn't exist.
UPLOAD_DIR = "uploads"

# Only these file types are allowed
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}

# Maximum file size: 20MB
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB in bytes


def save_document(
    file: UploadFile,
    category: str | None,
    current_user: User,
    db: Session
) -> Document:
    """
    Handles the full document upload process:
    
    1. Validate the file (type and size)
    2. Save the file to disk (uploads/ folder)
    3. Save file metadata to PostgreSQL
    4. Return the document record
    
    The file stays as "pending" status — 
    the AI pipeline (Step 4) will process it and change status to "completed"
    """

    # Step 1 — Validate file extension
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Step 2 — Create uploads folder if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Step 3 — Save file to disk
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Step 4 — Check file size after saving
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        os.remove(file_path)  # delete the oversized file
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large. Maximum size is 20MB."
        )

    # Step 5 — Save document metadata to PostgreSQL
    document = Document(
        filename=filename,
        category=category,
        status="pending",       # will be updated to "completed" after AI processing
        chunk_count=0,          # will be updated after chunking
        uploaded_by=current_user.id
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_all_documents(db: Session) -> list[Document]:
    """
    Returns all uploaded documents from the database.
    Used by GET /api/documents
    """
    return db.query(Document).order_by(Document.created_at.desc()).all()


def delete_document(document_id: int, db: Session) -> dict:
    """
    Deletes a document from both disk and database.
    Used by DELETE /api/documents/{id}
    """
    # Find the document in the database
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # Delete file from disk if it exists
    file_path = os.path.join(UPLOAD_DIR, document.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete from database
    db.delete(document)
    db.commit()

    return {"message": f"Document '{document.filename}' deleted successfully"}
