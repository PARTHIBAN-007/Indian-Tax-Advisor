from langgraph.graph import MessagesState
from typing import Annotated, Sequence,List,TypedDict,Optional
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List, Union
from pydantic import BaseModel
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AdvisorState(TypedDict):
    """
    State for the AdvisorState worklow
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]


