from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode
from config import settings
from langchain_core.messages import AIMessage
from application.conversation_service.workflows.chains import (
    get_response_chain,
    get_context_summary_chain,
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
    state["messages"].append(response)

  

    return state

from langchain_core.messages import HumanMessage

from langchain_core.messages import ToolMessage, AIMessage

async def summarize_context_node(state: AdvisorState, config: RunnableConfig):
    logger.info("Summarize Retrieved Context Node")
    print(state["messages"])

   
    tool_messages = [
        msg for msg in state["messages"]
        if isinstance(msg, ToolMessage) and msg.content and msg.content.strip()
    ]

    if not tool_messages:
        logger.warning("No valid tool content to summarize. Returning original state.")
        return state

    context_summary_chain = get_context_summary_chain()

    summary_input_messages = [HumanMessage(content=msg.content) for msg in tool_messages]

    summary_response = await context_summary_chain.ainvoke(
        {"messages": summary_input_messages},
        config
    )

    state["messages"] = [msg for msg in state["messages"] if not isinstance(msg, ToolMessage)]

    summarized_msg = AIMessage(content=summary_response.content)
    state["messages"].append(summarized_msg)

    return state



