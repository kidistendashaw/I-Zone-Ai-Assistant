from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):
    """
    What the backend returns after a document is uploaded.
    
    Example response:
    {
        "id": 1,
        "filename": "izone-services.pdf",
        "status": "pending",
        "chunk_count": 0,
        "created_at": "2026-09-02T10:00:00"
    }
    
    Note: status starts as "pending" → becomes "completed" after AI processing
    """
    id: int
    filename: str
    category: str | None
    status: str
    chunk_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """
    List of all uploaded documents.
    Used by GET /api/documents
    """
    documents: list[DocumentResponse]
    total: int
