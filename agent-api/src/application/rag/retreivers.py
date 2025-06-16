from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from loguru import logger
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from config import settings

from .embeddings import get_embedding_model


def get_retriever(
    embedding_model_id: str,
    k: int = 3,
    device: str = "cpu"):
    
    logger.info(
        f"Initializing retriever | model: {embedding_model_id} | device: {device} | top_k: {k}"
    )

    embedding_model = get_embedding_model(embedding_model_id, device)

    return vector_search_retriever(embedding_model, k)


def vector_search_retriever(
    embedding_model: HuggingFaceEmbeddings, k: int
) -> QdrantVectorStore :
    logger.info("Initializing vector store and retriever ")
    
    
    vector_store = QdrantVectorStore.from_existing_collection(
        embedding=embedding_model,
        collection_name=settings.QDRANT_COLLECTION_NAME,
        api_key=settings.QDRANT_CLIENT_API_KEY,
        url = settings.QDRANT_URI,
    )

    retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 3})
    print(retriever)
    return retriever
