import os
from sqlalchemy.orm import Session
from app.db.models import Document
from app.rag.chunker import extract_text_from_file, split_into_chunks
from app.rag.embedder import embed_chunks
from app.rag.vector_store import store_chunks, delete_document_chunks

UPLOAD_DIR = "uploads"


def process_document(document_id: int, db: Session) -> None:
    """
    The full AI pipeline for a single document.
    Called after a document is uploaded.
    
    Steps:
    1. Load document from database
    2. Extract text from the file on disk
    3. Split text into chunks
    4. Embed each chunk (text → vector)
    5. Store vectors in ChromaDB
    6. Update document status to "completed"
    
    If anything goes wrong, status is set to "failed".
    """

    # Step 1 — Load document from database
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        print(f"Document {document_id} not found")
        return

    # Update status to "processing"
    document.status = "processing"
    db.commit()

    try:
        # Step 2 — Extract text from file
        file_path = os.path.join(UPLOAD_DIR, document.filename)
        print(f"Processing: {file_path}")
        text = extract_text_from_file(file_path)

        if not text.strip():
            raise ValueError("No text could be extracted from the file")

        # Step 3 — Split text into chunks
        chunks = split_into_chunks(text, document_id)
        print(f"Created {len(chunks)} chunks")

        # Step 4 — Embed each chunk (text → vector using Ollama)
        print("Embedding chunks with Ollama...")
        chunks_with_embeddings = embed_chunks(chunks)

        # Step 5 — Store vectors in ChromaDB
        print("Storing in ChromaDB...")
        store_chunks(chunks_with_embeddings)

        # Step 6 — Update document status to "completed"
        document.status = "completed"
        document.chunk_count = len(chunks)
        db.commit()
        print(f"Document {document_id} processed successfully — {len(chunks)} chunks stored")

    except Exception as e:
        # If anything fails, mark as "failed" so admin knows to re-upload
        document.status = "failed"
        db.commit()
        print(f"Failed to process document {document_id}: {str(e)}")
        raise


def remove_document_from_vectorstore(document_id: int) -> None:
    """
    Removes a document's chunks from ChromaDB.
    Called when admin deletes a document.
    """
    delete_document_chunks(document_id)
    print(f"Removed chunks for document {document_id} from ChromaDB")
