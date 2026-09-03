import ollama


# This is the embedding model we use.
# nomic-embed-text is fast, free, and runs locally via Ollama.
# It converts text into a list of 768 numbers that represent its meaning.
EMBEDDING_MODEL = "nomic-embed-text"


def embed_text(text: str) -> list[float]:
    """
    Converts a piece of text into a vector (list of numbers).
    
    Example:
        embed_text("I-Zone offers development teams")
        → [0.23, 0.87, 0.12, 0.56, 0.34, ...]  (768 numbers)
    
    Two texts with similar meaning will have similar vectors.
    This is how ChromaDB finds relevant chunks for a question.
    """
    response = ollama.embeddings(
        model=EMBEDDING_MODEL,
        prompt=text
    )
    return response["embedding"]


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Takes a list of chunks and adds an embedding to each one.
    
    Input:
        [{"id": "doc_1_chunk_0", "text": "I-Zone offers...", "metadata": {...}}]
    
    Output:
        [{"id": "doc_1_chunk_0", "text": "...", "metadata": {...}, "embedding": [0.23, ...]}]
    """
    embedded = []
    for chunk in chunks:
        embedding = embed_text(chunk["text"])
        embedded.append({
            **chunk,
            "embedding": embedding
        })
    return embedded
