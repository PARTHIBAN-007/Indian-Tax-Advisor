from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from config import settings


def get_qdrant_client():
    qdrant = QdrantClient(
        api_key=settings.QDRANT_CLIENT_API_KEY,
        url = settings.QDRANT_URI,
    )

    qdrant.recreate_collection(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    print(qdrant.get_collections())

    return qdrant