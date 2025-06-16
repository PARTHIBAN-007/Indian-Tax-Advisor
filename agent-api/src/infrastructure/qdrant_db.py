from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from config import settings


def get_qdrant_client():
    qdrant = QdrantClient(
        api_key=settings.QDRANT_CLIENT_API_KEY,
        url = settings.QDRANT_URI,
    )

    if settings.QDRANT_COLLECTION_NAME not in [col.name for col in qdrant.get_collections().collections]:
        qdrant.create_collection(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )


    collection_info = qdrant.get_collection(settings.QDRANT_COLLECTION_NAME)
    print("Points 1:", collection_info.points_count)





    return qdrant
