import chromadb

# ChromaDB stores data on disk in this folder.
# It persists between server restarts.
CHROMA_PATH = "chroma_db"

# All I-Zone document chunks go into this collection.
# Think of it like a table in PostgreSQL, but for vectors.
COLLECTION_NAME = "izone_documents"


def get_collection():
    """
    Returns the ChromaDB collection where all document chunks are stored.
    Creates the collection if it doesn't exist yet.
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}  # use cosine similarity for search
    )
    return collection


def store_chunks(chunks_with_embeddings: list[dict]) -> None:
    """
    Saves embedded chunks into ChromaDB.
    
    Each chunk is stored with:
        - id: unique identifier (e.g. "doc_1_chunk_0")
        - embedding: the vector [0.23, 0.87, ...]
        - document: the original text
        - metadata: document_id, chunk_index
    """
    collection = get_collection()

    ids = [chunk["id"] for chunk in chunks_with_embeddings]
    embeddings = [chunk["embedding"] for chunk in chunks_with_embeddings]
    documents = [chunk["text"] for chunk in chunks_with_embeddings]
    metadatas = [chunk["metadata"] for chunk in chunks_with_embeddings]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )


def search_similar_chunks(query_embedding: list[float], n_results: int = 5) -> list[str]:
    """
    Finds the most relevant chunks for a given query embedding.
    
    This is called when a user asks a question:
    1. Question is converted to a vector (in embedder.py)
    2. This function finds the n closest chunks in ChromaDB
    3. Those chunks are sent to Ollama to generate the answer
    
    Returns a list of text strings (the relevant chunks).
    """
    collection = get_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    # results["documents"] is a list of lists — we flatten to a simple list
    return results["documents"][0] if results["documents"] else []


def delete_document_chunks(document_id: int) -> None:
    """
    Removes all chunks belonging to a document from ChromaDB.
    Called when an admin deletes a document.
    """
    collection = get_collection()
    collection.delete(
        where={"document_id": document_id}
    )
