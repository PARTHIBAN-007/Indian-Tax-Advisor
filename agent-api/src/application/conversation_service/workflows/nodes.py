from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode
from config import settings
from langchain_core.messages import AIMessage
from application.conversation_service.workflows.chains import (
    get_response_chain,
    get_conversation_summary_chain
)

from application.conversation_service.workflows.state import AdvisorState

from application.conversation_service.workflows.tools import tool_node
from loguru import logger
tool_node = ToolNode(tool_node)


async def conversation_node(state:AdvisorState,config:RunnableConfig):
    logger.info("Conversation Node")
    conversation_chain = get_response_chain()
    
   


    response = await conversation_chain.ainvoke(
        {   
            "messages":state["messages"],
        },
        config 
    )
    print(response)
    state["messages"].append(response)
    print("Response Added ?")
    print(state["messages"])

    return state

async def summarize_conversation_node(state:AdvisorState,config:RunnableConfig):
    logger.info("Conversation summarry Node")
    summary_chain = get_conversation_summary_chain()

    response = await summary_chain.ainvoke(
        {
            "messages":state["messages"],
        },
        config
    )

    return state
