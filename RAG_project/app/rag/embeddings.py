from langchain_openai import OpenAIEmbeddings
from app.config import settings

def get_embeddings_model():
    return OpenAIEmbeddings(model=settings.EMBEDDING_MODEL)
