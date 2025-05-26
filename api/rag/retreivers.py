from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.vectorstores import Qdrant
from api.config import settings
from rag.embeddings import get_embedding_model
def get_retriever(
        embedding_model_id: str,
        k: int = 3,
        device: str = "cpu"
):
    embedding_model = get_embedding_model(embedding_model_id,device)

    return get_hybrid_search_retriever(embedding_model,k)

def get_hybrid_search_retriever(
        embedding_model: HuggingFaceEmbeddings,
        k: int
):
    vector_store = Qdrant(
        client = settings.QDRANT_CLIENT_PATH,
        collection_name="",
        embedding_model = embedding_model,


    )
    retriever = vector_store.as_retriever(
        search_kwargs = {"k":k},
        search_index = "mmr"
    )
    return retriever
    