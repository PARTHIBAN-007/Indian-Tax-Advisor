from langchain.agents import Tool
from langchain_community.tools import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchRun
from application.rag.retreivers import get_retriever
from langchain_core.tools import tool
from config import settings
from loguru import logger
from dotenv import load_dotenv
load_dotenv()
import os
tailvy_api_key = settings.TAVILY_API_KEY
os.environ["TAVILY_API_KEY"] = tailvy_api_key
from application.conversation_service.workflows.state import AdvisorState

@tool
def retriever_tool(query: str):
    """Search the Vector Database to understand the user preferences and specific information about the user."""
    logger.info("Retriever Tool")
    retriever = get_retriever(
        embedding_model_id=settings.RAG_TEXT_EMBEDDING_MODEL,
        k=settings.RAG_TOP_K,
    )
    retrieved_docs = retriever.invoke(query)

    # ✅ Don't modify state or call AdvisorState.append
    logger.info(f"Retrieved Docs: {retrieved_docs}")
    
    return retrieved_docs

@tool
def web_search_tool(query:str)->str:
    """
    Use this web_Search tool to get real time updates using tailvy search tool
    """
    logger.info("Web search Tool")
    tavily_search_docs = TavilySearchResults(
     max_results=3,
    include_answer=True).invoke(input=query)
    logger.info("Retrieved web search data")

    return tavily_search_docs



tool_node = [retriever_tool,web_search_tool]