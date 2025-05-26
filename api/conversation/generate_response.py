import uuid
from typing import Union, Any
from api.config import settings
from langchain_core.messages import AIMessage , HumanMessage 
from langgraph.checkpoint.mongodb.aio import AsyncMongoDBSaver
from conversation.workflows.graph import create_workflow_graph
from opik.integrations.langchain import OpikTracer


async def get_response(
        messages: str | list[str] | list[dict[str,Any]]
) -> tuple[str]:
    graph_builder = create_workflow_graph()

    try:
        async with AsyncMongoDBSaver.from_conn_string(
            conn_string = settings.MONGO_URI,
            db_name = settings.MONGO_DB_NAME,
            checkpoint_collection_name = settings.MONGO_STATE_CHECKPOINT_COLLECTION,
            writes_collection_name = settings.MONGO_STATE_WRITES_COLLECTION
        ) as checkpointer:
            
            opik_tracer = OpikTracer(graph=graph.get_graph(xray= True))
            graph = graph_builder.compile(checkpointer=checkpointer)
            thread_id = uuid.uuid4
            config = {
                "configurable" : {"thread_id":thread_id},
                "callbacks": {opik_tracer}
            }

            output_state = await graph.invoke(
                input = {
                    "messages" : __format_messages(messages=messages),
                },
                config = config
            )

        last_message = output_state["messages"][-1]
        return last_message.content
    except Exception as e:
        raise RuntimeError(f"Error running Conversation Workflow : {str(e)}")
    



def __foramt_messages(
        messages: Union[str,list[dict[str,Any]]],
) -> list[Union[HumanMessage,AIMessage]]:
    
    if isinstance(messages,str):
        return [HumanMessage(content = messages)]
    
    if isinstance(messages, list):
        if not messages:
            return []
        
        if (
            isinstance(messages[0],dict)
            and "role" in messages[0]
            and "content" in messages[0]
        ):
            result = []
            for msg in messages:
                if msg["role"] == "user":
                    result.append(HumanMessage(content = msg["content"]))
                elif msg["role"]=="assistant":
                    result.append(AIMessage(content= msg["content"]))
            return result
        
        return [HumanMessage(content=message) for message in messages]
    return  []    
