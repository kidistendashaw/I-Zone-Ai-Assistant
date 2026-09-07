import ollama

# This is the LLM model that generates answers.
# llama3.2 is a powerful local model that runs on your machine for free.
CHAT_MODEL = "llama3.2"


def generate_answer(question: str, context_chunks: list[str]) -> str:
    """
    Sends the user's question + relevant document chunks to Ollama.
    Ollama reads the context and writes an answer.

    Parameters:
        question: what the user asked
        context_chunks: relevant text from I-Zone documents (from ChromaDB)

    Returns:
        A string answer from the AI

    Example:
        question = "What services does I-Zone offer?"
        context_chunks = ["I-Zone offers dedicated development teams...",
                          "Our services include SaaS, AI products..."]
        → "I-Zone offers dedicated development teams, SaaS platforms,
           AI products, and ERP systems..."
    """

    # If no relevant chunks found, tell the user honestly
    if not context_chunks:
        return (
            "I don't have enough information to answer that question. "
            "Please make sure relevant documents have been uploaded."
        )

    # Build the context string from all chunks
    context = "\n\n".join(context_chunks)

    # This is the prompt we send to Ollama.
    # We tell it to ONLY use the provided context — not make things up.
    prompt = f"""You are an AI assistant for I-Zone Technologies.
Answer the user's question based ONLY on the context provided below.
If the answer is not in the context, say "I don't have that information in the uploaded documents."
Do not make up information.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:"""

    response = ollama.chat(
        model=CHAT_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]
