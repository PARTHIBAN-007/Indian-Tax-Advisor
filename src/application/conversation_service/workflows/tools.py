from langchain.agents import Tool
from langchain_community.tools import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchRun
from application.rag.retreivers import get_retriever
from langchain_core.tools import tool
from langchain.tools.retriever import create_retriever_tool
from config import settings

from dotenv import load_dotenv
load_dotenv()
import os
tailvy_api_key = settings.TAVILY_API_KEY
os.environ["TAVILY_API_KEY"] = tailvy_api_key


retriever = get_retriever(
    embedding_model_id=settings.RAG_TEXT_EMBEDDING_MODEL,
    k = settings.RAG_TOP_K,
)

retriever_tool = create_retriever_tool(
    retriever,
    name = "Retrieve_user_context",
    description = "Search the Vector Database to understand the user preferences and specific information about the user.Always use this tool when you need any information related to user specific details"
)


@tool
def web_search_tool(query:str)->str:
    """
    Use this web_Search tool to get real time updates using tailvy search tool
    """
    tavily_search_docs = TavilySearchResults(
     max_results=5,
    include_answer=True,
    include_raw_content=True).invoke(input=query)
    print(tavily_search_docs)
    return tavily_search_docs



tool_node = [retriever_tool,web_search_tool]