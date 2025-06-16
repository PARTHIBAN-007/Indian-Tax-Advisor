from application.conversation_service.workflows.chains import get_conversation_summary_chain
from application.rag.embeddings import get_embedding_model
from infrastructure.qdrant_db import get_qdrant_client
from config import settings
import uuid 

async def embed_conversation():
    try:
        summarized_conversation = get_conversation_summary_chain()
        embedding_model = get_embedding_model()

        vectors = embedding_model.embed_query(summarized_conversation)
        client = get_qdrant_client()

        client.upsert(
            collection_name = settings.QDRANT_COLLECTION_NAME,
            points = [
                {
                    "id":uuid.uuid4,
                    "vector":vectors,
                    "payload": {
                        "type":"summary",
                        "content": summarized_conversation,
                    }
                }
            ]

        )
    except Exception as e:
        raise RuntimeError(f"Error in Embedding and loading the Conversation: {str(e)}")





