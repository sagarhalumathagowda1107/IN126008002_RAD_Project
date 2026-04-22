import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from app.config import settings
from app.utils.logger import logger

def ingest_pdf(file_path: str, session_id: str) -> List[Document]:
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        # Attach metadata
        for i, doc in enumerate(documents):
            doc.metadata['session_id'] = session_id
            doc.metadata['filename'] = os.path.basename(file_path)
            doc.metadata['chunk_id'] = f"{session_id}_{os.path.basename(file_path)}_{i}"
        
        return documents
    except Exception as e:
        logger.error(f"Error ingesting PDF {file_path}: {e}")
        return []
