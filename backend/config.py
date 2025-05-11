from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    GROQ_API_KEY: str
    GROQ_LLM_MODEL:str = "llama-3.3-70b-versatile"
    GROQ_LLM_MODEL_CONTEXT_SUMMARY:str = "llama-3.1-8b-instant"


    MONGO_URI: str = Field(
        default="mongodb://philoagents:philoagents@local_dev_atlas:27017/?directConnection=true",
        description="Connection URI for the local MongoDB Atlas instance.",
    )
    
    MONGO_DB_NAME: str = "philoagents"
    MONGO_STATE_CHECKPOINT_COLLECTION: str = "philosopher_state_checkpoints"
    MONGO_STATE_WRITES_COLLECTION: str = "philosopher_state_writes"
    MONGO_LONG_TERM_MEMORY_COLLECTION: str = "philosopher_long_term_memory"

    TOTAL_MESSAGES_SUMMARY_TRIGGER: int = 30
    TOTAL_MESSAGES_AFTER_SUMMARY: int = 5

    RAG_TEXT_EMBEDDING_MODEL:str = "sentence-transformers/all-MiniLM-L6-v2"
    RAG_TEXT_EMBEDDING_MODEL_DIM:int = 384
    RAG_TOP_K:int =5
    RAG_CHUNK_SIZE:int = 256

    QDRANT_CLIENT_PATH:str = "Long Term Memory"

settings = Settings()