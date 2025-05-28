from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv
load_dotenv()

tailvy_api_key = os.getenv("TAVILY_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
comet_api_key = os.getenv("COMET_API_KEY")
class Settings(BaseSettings):

    GROQ_API_KEY: str = groq_api_key
    GROQ_LLM_MODEL:str = "llama-3.3-70b-versatile"
    GROQ_LLM_MODEL_CONTEXT_SUMMARY:str = "llama-3.1-8b-instant"
    TAVILY_API_KEY : str = tailvy_api_key


    MONGO_URI: str = Field(
        default="localhost:27017",
        description="Connection URI for the local MongoDB Atlas instance.",
    )
    
    COMET_API_KEY: str = comet_api_key
    COMET_PROJECT: str = Field(
        default="Indian Tax System",
        description="Project name for Comet ML and Opik tracking.",
    )

    MONGO_DB_NAME: str = "indian_tax_system"
    MONGO_STATE_CHECKPOINT_COLLECTION: str = "tax_state_checkpoints"
    MONGO_STATE_WRITES_COLLECTION: str = "tax_state_writes"
    MONGO_LONG_TERM_MEMORY_COLLECTION: str = "tax_long_term_memory"

    TOTAL_MESSAGES_SUMMARY_TRIGGER: int = 30
    TOTAL_MESSAGES_AFTER_SUMMARY: int = 5

    RAG_TEXT_EMBEDDING_MODEL:str = "sentence-transformers/all-MiniLM-L6-v2"
    RAG_TEXT_EMBEDDING_MODEL_DIM:int = 384
    RAG_TOP_K:int =5
    RAG_CHUNK_SIZE:int = 256

    QDRANT_CLIENT_PATH:str = "Long_Term_Memory"

settings = Settings()