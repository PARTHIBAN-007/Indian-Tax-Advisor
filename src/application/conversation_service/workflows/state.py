from langgraph.graph import MessagesState
from typing import Annotated, Sequence,List,TypedDict,Optional
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List, Union
from pydantic import BaseModel
from langchain_core.messages import BaseMessage

class AdvisorState(TypedDict):
    """
    State for the AdvisorState worklow
    """
    messages: List[BaseMessage] = []


