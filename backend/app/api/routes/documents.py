from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.api.deps import get_current_admin, get_current_user
from app.services.document import save_document, get_all_documents, delete_document
from app.schemas.document import DocumentResponse, DocumentListResponse

router = APIRouter(prefix="/api/documents", tags=["Documents"])


@router.post("", response_model=DocumentResponse, status_code=201)
def upload_document(
    file: UploadFile = File(...),
    category: str | None = Form(None),
    current_user: User = Depends(get_current_admin),  # admin only
    db: Session = Depends(get_db)
):
    """
    UPLOAD A DOCUMENT (Admin only)
    
    The frontend sends a multipart form with:
        - file: the PDF/TXT/DOCX file
        - category: optional label e.g. "services", "pricing", "policies"
    
    Returns the saved document metadata.
    Status will be "pending" until the AI pipeline processes it.
    
    Only admins can upload documents.
    """
    return save_document(file, category, current_user, db)


@router.get("", response_model=DocumentListResponse)
def list_documents(
    current_user: User = Depends(get_current_user),  # any logged-in user
    db: Session = Depends(get_db)
):
    """
    LIST ALL DOCUMENTS
    
    Returns all uploaded documents with their status.
    Any logged-in user can see the list.
    """
    documents = get_all_documents(db)
    return DocumentListResponse(documents=documents, total=len(documents))


@router.delete("/{document_id}")
def remove_document(
    document_id: int,
    current_user: User = Depends(get_current_admin),  # admin only
    db: Session = Depends(get_db)
):
    """
    DELETE A DOCUMENT (Admin only)
    
    Removes the document from both disk and database.
    """
    return delete_document(document_id, db)
