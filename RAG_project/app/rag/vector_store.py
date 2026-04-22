import os
import shutil
from langchain_chroma import Chroma
from app.rag.embeddings import get_embeddings_model
from app.config import settings
from langchain_core.documents import Document
from typing import List

def get_vector_store(session_id: str) -> Chroma:
    # Use session_id as the collection name
    return Chroma(
        collection_name=f"session_{session_id.replace('-', '_')}",
        embedding_function=get_embeddings_model(),
        persist_directory=settings.CHROMA_DB_DIR
    )

def add_documents_to_store(session_id: str, documents: List[Document]):
    vector_store = get_vector_store(session_id)
    vector_store.add_documents(documents)

def clear_session_collection(session_id: str):
    vector_store = get_vector_store(session_id)
    vector_store.delete_collection()
