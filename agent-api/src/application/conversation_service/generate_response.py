import uuid
from typing import Union, Any
from config import settings
from langchain_core.messages import AIMessage , HumanMessage 
from application.conversation_service.workflows.graph import create_workflow_graph
from application.conversation_service.workflows.state import AdvisorState
from application.conversation_service.workflows.chains import get_conversation_summary_chain
from opik.integrations.langchain import OpikTracer
from application.rag.embeddings import get_embedding_model
from infrastructure.qdrant_db import get_qdrant_client
from config import settings
import uuid 
from loguru import logger
import os
from langgraph.checkpoint.memory import MemorySaver
import opik
from loguru import logger
from opik.configurator.configure import OpikConfigurator

from config import settings


def configure() -> None:
    if settings.COMET_API_KEY and settings.COMET_PROJECT:
        print(settings.COMET_API_KEY)
        client = OpikConfigurator(api_key=settings.COMET_API_KEY)
        default_workspace = client._get_default_workspace()
       
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




class GraphBuilding():
    def __init__(self,id):
        self.id = id
        self.graph_builder = create_workflow_graph()
    
        configure()
        memory = MemorySaver()
        self.graph = self.graph_builder.compile(checkpointer=memory)
        self.opik_tracer = OpikTracer(graph=self.graph.get_graph(xray=True))  
        self.thread_id = uuid.uuid4()
        self.config = {
            "configurable" : {"thread_id":self.thread_id},
            "callbacks": [self.opik_tracer],
        }  

        self.embedding_model = get_embedding_model(model_id=settings.RAG_TEXT_EMBEDDING_MODEL)
        logger.info(self.config) 

    async def generate_response(self,messages: str | list[str] | list[dict[str,Any]]):
        try:
            self.output_state =  await self.graph.ainvoke(
                input = {
                    "messages" : self.__format_messages(messages=messages),
                },
                config = self.config
            )
            print(self.output_state)
            logger.info("-------------------OUptut-----------------------",self.output_state)

            last_message = self.output_state["messages"][-1]

            print(last_message)
            return last_message.content
        except Exception as e:
            raise RuntimeError(f"Error running Conversation Workflow : {str(e)}")
        
    def embed_conversation(self):
        try:
            print(self.output_state["messages"])
            summarize_chain = get_conversation_summary_chain()
            summarized_context = [doc.content for doc in self.output_state["messages"]]
            print("*"*2000)
            print(summarized_context)


            
            summarized_conversation = summarize_chain.invoke(summarized_context)
            print(summarized_conversation.content)
            embedding_model = self.embedding_model
            vectors = embedding_model.embed_query(summarized_conversation.content)
            if not isinstance(vectors, list):
                vectors = vectors.tolist()

            print(len(vectors), type(vectors), vectors[:5])


            client = get_qdrant_client()

            client.upsert(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                points=[
                    {
                        "id": str(uuid.uuid4()),
                        "vector": vectors,
                        "payload": {
                            "user_id": self.id,
                            "type": "summary",
                            "page_content": str(summarized_conversation.content),  
                        }
                    }
                ]
            )

            collection_info = client.get_collection(settings.QDRANT_COLLECTION_NAME)
            print("Points 2:", collection_info.points_count)


            self.thread_id = uuid.uuid4()
            self.config = {
                "configurable" : {"thread_id":self.thread_id},
                "callbacks": [self.opik_tracer],
            } 
        except Exception as e:
            raise RuntimeError(f"Error in Embedding and loading the Conversation: {str(e)}")

        

    
    def __format_messages(self,
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


