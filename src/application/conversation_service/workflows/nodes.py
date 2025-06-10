from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode
from config import settings
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
    print(state["messages"])
    logger.info("Before COncersafsg")
    conversation_chain = get_response_chain()
    logger.info("Conversation Node")
    


    response = await conversation_chain.ainvoke(
        {   
            "messages":state["messages"],
        },
        config 
    )
    print(response)

    return {"messages":response}

async def summarize_conversation_node(state:AdvisorState,config:RunnableConfig):
    logger.info("Conversation summry Node")
    summary = state.get("summary","")
    summary_chain = get_conversation_summary_chain(summary)

    response = await summary_chain.ainvoke(
        {
            "messages":state["messages"],
            "summary":summary
        },
        config
    )

    delete_messages = [
        RemoveMessage(
            id=message.id,
            reason="summarization",
        )
        for message in state["messages"][: -settings.TOTAL_MESSAGES_AFTER_SUMMARY]
    ]

    return {"summary":response.content,"messages":delete_messages}


async def summarize_context_node(state:AdvisorState,config:RunnableConfig):
    logger.info("Summarize Retrieved Context Node")
    context_summary_chain = get_context_summary_chain()
    print(state["messages"])
    response = await context_summary_chain.ainvoke(
        {
           "context": state["messages"][-1].content,
        },
        config
    )

    state["messages"][-1].content = response.content

    return {}

async def connector_node(state: AdvisorState):
    return {}


async def generate_response(state:AdvisorState,config:RunnableConfig):
    user_chat_history = state["user_chat_history"]
    web_search_results = state["web_search_results"]

    conversation_chain = get_response_chain()


    response = conversation_chain.ainvoke(
        {
            "user_chat_history":user_chat_history,
            "web_search_results":web_search_results
        },
        config
    )

    return {"messages":response}