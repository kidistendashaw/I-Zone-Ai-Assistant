import os
from PyPDF2 import PdfReader
from docx import Document as DocxDocument

# Each chunk will be this many characters long
CHUNK_SIZE = 1000

# Chunks overlap by this many characters so context isn't lost at boundaries
CHUNK_OVERLAP = 200

# Only these file types are allowed
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}


def extract_text_from_file(file_path: str) -> str:
    """
    Reads a file and returns all its text content as a string.
    Supports PDF, TXT and DOCX files.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return _extract_from_pdf(file_path)
    elif ext == ".txt":
        return _extract_from_txt(file_path)
    elif ext == ".docx":
        return _extract_from_docx(file_path)
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


def _extract_from_docx(file_path: str) -> str:
    """Reads a Word document and returns all paragraph text."""
    doc = DocxDocument(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"
    return text


def split_into_chunks(text: str, document_id: int) -> list[dict]:
    """
    Splits a long text into smaller overlapping chunks.
    Returns a list of dicts ready to be stored in ChromaDB.
    """
    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk_text = text[start:end].strip()

        if chunk_text:
            chunks.append({
                "id": f"doc_{document_id}_chunk_{chunk_index}",
                "text": chunk_text,
                "metadata": {
                    "document_id": document_id,
                    "chunk_index": chunk_index
                }
            })
            chunk_index += 1

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks
