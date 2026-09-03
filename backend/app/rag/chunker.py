import os
from PyPDF2 import PdfReader


# Each chunk will be this many characters long
CHUNK_SIZE = 1000

# Chunks overlap by this many characters so context isn't lost at boundaries
# Example: if chunk 1 ends with "I-Zone offers..." chunk 2 starts a bit before that
CHUNK_OVERLAP = 200


def extract_text_from_file(file_path: str) -> str:
    """
    Reads a file and returns all its text content as a string.
    Supports PDF and TXT files.
    
    Example:
        extract_text_from_file("uploads/izone-services.pdf")
        → "I-Zone Technologies offers dedicated development teams..."
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return _extract_from_pdf(file_path)
    elif ext == ".txt":
        return _extract_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def _extract_from_pdf(file_path: str) -> str:
    """Reads all pages of a PDF and returns the text."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def _extract_from_txt(file_path: str) -> str:
    """Reads a plain text file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def split_into_chunks(text: str, document_id: int) -> list[dict]:
    """
    Splits a long text into smaller overlapping chunks.
    
    Why overlap? So that if an answer spans two chunks, neither chunk
    loses the context from the previous one.
    
    Returns a list of dicts like:
    [
        {
            "id": "doc_1_chunk_0",
            "text": "I-Zone Technologies offers...",
            "metadata": {"document_id": 1, "chunk_index": 0}
        },
        ...
    ]
    
    These dicts are what get stored in ChromaDB.
    """
    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk_text = text[start:end].strip()

        if chunk_text:  # skip empty chunks
            chunks.append({
                "id": f"doc_{document_id}_chunk_{chunk_index}",
                "text": chunk_text,
                "metadata": {
                    "document_id": document_id,
                    "chunk_index": chunk_index
                }
            })
            chunk_index += 1

        # Move forward but overlap with previous chunk
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks
