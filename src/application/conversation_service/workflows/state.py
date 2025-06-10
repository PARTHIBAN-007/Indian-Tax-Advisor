from langgraph.graph import MessagesState
from typing import Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage


class AdvisorState(MessagesState):
    """
    State for the AdvisorState worklow
    """
    user_query:str = None
    web_search_results: str = None
    user_chat_history:str = None
    summary : str = None

