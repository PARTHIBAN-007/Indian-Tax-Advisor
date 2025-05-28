from langchain.agents import Tool
from langchain_community.tools import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchRun
from application.rag.retreivers import get_retriever
from langchain.tools.retriever import create_retriever_tool
from config import settings

from dotenv import load_dotenv
load_dotenv()
import os
tailvy_api_key = settings.TAVILY_API_KEY
os.environ["TAVILY_API_KEY"] = tailvy_api_key

tools = [TavilySearchResults(
     max_results=5,
    include_answer=True,
    include_raw_content=True,
    include_images=True
)]

retriever = get_retriever(
    embedding_model_id=settings.RAG_TEXT_EMBEDDING_MODEL,
    k = settings.RAG_TOP_K,
)

retriever_tool = create_retriever_tool(
    retriever,
    "Retrieve_user_context",
    "Search the Vector Database to understand the user preferences and specific information about the user.Always use this tool when you need any information related to user specific details"
)


retriever_tools = [retriever_tool]

web_search_tools = [DuckDuckGoSearchRun()]
