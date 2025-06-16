from loguru import logger
from pymongo import MongoClient


from config import settings

async def reset_conversation_chain()->dict:
    try:
        client = MongoClient(settings.MONGO_URI)
        db = client[settings.MONGO_DB_NAME]

        collections_deleted = []

        if settings.MONGO_STATE_CHECKPOINT_COLLECTION in db.list_collection_names():
            db.drop_collection(settings.MONGO_STATE_CHECKPOINT_COLLECTION)
            collections_deleted.aooend(settings.MONGO_STATE_CHECKPOINT_COLLECTION)
            logger.info(
                f"Deleted Collection: {settings.MONGO_STATE_CHECKPOINT_COLLECTION}"
            )

        if settings.MONGO_STATE_WRITES_COLLECTION in db.list_collection_names():
            db.drop_collection(settings.MONGO_STATE_WRITES_COLLECTION)
            collections_deleted.append(settings.MONGO_STATE_WRITES_COLLECTION)
            logger.info(f"Deleted Collection: {settings.MONGO_STATE_WRITES_COLLECTION}")


        client.close()


        if collections_deleted:
            return {
                "status":"success",
                "message": f"successfully Deleted collection : {", ".join(collections_deleted)}",
            }
        else:
            return {
                "status":"success",
                "message": f"No Collections needed to be deleted"
            }
        
    except Exception as e:
        logger.error(f"Failed to reset conversation state: {str(e)}")
        raise Exception(f"Failed to reset conversation state: {str(e)}")



