import uuid
from typing import Union, Any
from config import settings
from langchain_core.messages import AIMessage , HumanMessage 
from langgraph.checkpoint.mongodb.aio import AsyncMongoDBSaver
from application.conversation_service.workflows.graph import create_workflow_graph
from opik.integrations.langchain import OpikTracer
from loguru import logger
import os

import opik
from loguru import logger
from opik.configurator.configure import OpikConfigurator

from config import settings


def configure() -> None:
    if settings.COMET_API_KEY and settings.COMET_PROJECT:
        try:
            client = OpikConfigurator(api_key=settings.COMET_API_KEY)
            default_workspace = client._get_default_workspace()
        except Exception:
            logger.warning(
                "Default workspace not found. Setting workspace to None and enabling interactive mode."
            )
            default_workspace = None

        os.environ["OPIK_PROJECT_NAME"] = settings.COMET_PROJECT

        try:
            opik.configure(
                api_key=settings.COMET_API_KEY,
                workspace=default_workspace,
                use_local=False,
                force=True,
            )
            logger.info(
                f"Opik configured successfully using workspace '{default_workspace}'"
            )
        except Exception:
            logger.warning(
                "Couldn't configure Opik. There is probably a problem with the COMET_API_KEY or COMET_PROJECT environment variables or with the Opik server."
            )
    else:
        logger.warning(
            "COMET_API_KEY and COMET_PROJECT are not set. Set them to enable prompt monitoring with Opik (powered by Comet ML)."
        )

async def get_response(
        messages: str | list[str] | list[dict[str,Any]]
) -> tuple[str]:
    graph_builder = create_workflow_graph()
    logger.info("Graph is Building")
    configure()

    try:
        async with AsyncMongoDBSaver.from_conn_string(
            conn_string = settings.MONGO_URI,
            db_name = settings.MONGO_DB_NAME,
            checkpoint_collection_name = settings.MONGO_STATE_CHECKPOINT_COLLECTION,
            writes_collection_name = settings.MONGO_STATE_WRITES_COLLECTION
        ) as checkpointer:
            

            graph = graph_builder.compile(checkpointer=checkpointer)
            opik_tracer = OpikTracer(graph=graph.get_graph(xray=True))            
        
            thread_id = uuid.uuid4
            config = {
                "configurable" : {"thread_id":thread_id},
                "callbacks": [opik_tracer],
            }
            print(config)
            output_state = await graph.ainvoke(
                input = {
                    "messages" : __format_messages(messages=messages),
                },
                config = config
            )

            




            logger.info("_------------------OUptut-----------------------",output_state)

        last_message = output_state["messages"][-1]
        print(last_message)
        return last_message.content
    except Exception as e:
        raise RuntimeError(f"Error running Conversation Workflow : {str(e)}")
    


def __format_messages(
    messages: Union[str, list[dict[str, Any]]],
) -> list[Union[HumanMessage, AIMessage]]:
   

    if isinstance(messages, str):
        return [HumanMessage(content=messages)]

    if isinstance(messages, list):
        if not messages:
            return []

        if (
            isinstance(messages[0], dict)
            and "role" in messages[0]
            and "content" in messages[0]
        ):
            result = []
            for msg in messages:
                if msg["role"] == "user":
                    result.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    result.append(AIMessage(content=msg["content"]))
            return result

        return [HumanMessage(content=message) for message in messages]

    return []
