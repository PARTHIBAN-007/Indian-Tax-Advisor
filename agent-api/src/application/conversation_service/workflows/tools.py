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

import json
@tool
def retriever_tool(query: str) -> str:
    """Search the Vector Database to understand the user preferences and specific information about the user."""
    logger.info("Retriever Tool")
    retriever = get_retriever(
        embedding_model_id=settings.RAG_TEXT_EMBEDDING_MODEL,
        k=settings.RAG_TOP_K,
    )
    retrieved_docs = retriever.invoke(query)
    logger.info(f"Retrieved Docs: {retrieved_docs}")

    return json.dumps(retrieved_docs, default=str) 

@tool
def web_search_tool(query: str) -> str:
    """
    Use this web search tool to get real-time updates using Tavily.
    """
    logger.info("Web Search Tool")
    tavily_search_docs = TavilySearchResults(
        max_results=3,
        include_answer=True
    ).invoke(input=query)
    logger.info("Retrieved web search data")

    # Convert to a string
    return json.dumps(tavily_search_docs, default=str)



tool_node = [retriever_tool,web_search_tool]