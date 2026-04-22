from app.rag.vector_store import get_vector_store
from typing import List, Dict, Any, Tuple
from langchain_core.documents import Document

def retrieve_chunks(session_id: str, query: str, top_k: int = 4) -> List[Tuple[Document, float]]:
    vector_store = get_vector_store(session_id)
    # Return documents and similarity scores
    results = vector_store.similarity_search_with_relevance_scores(query, k=top_k)
    return results
