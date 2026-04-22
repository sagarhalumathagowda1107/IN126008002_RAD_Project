def format_context(retrieved_chunks: list) -> str:
    context = ""
    for chunk in retrieved_chunks:
        context += f"Document: {chunk.get('filename', 'Unknown')}\n"
        context += f"Content: {chunk.get('text', '')}\n\n"
    return context
