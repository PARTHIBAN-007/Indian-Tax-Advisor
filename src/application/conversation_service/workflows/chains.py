from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from config import settings
from loguru import logger
from domain.prompts import SYSTEM_PROMPT ,CONTEXT_SUMMARY_PROMPT,EXTEND_CONTEXT_SUMMARY_PROMPT
from application.conversation_service.workflows.tools import tool_node

def get_chat_model(temperature: float=0.7,model_name:str = settings.GROQ_LLM_MODEL)->ChatGroq:
    logger.info("Chat Model ")
    return ChatGroq(
        api_key = settings.GROQ_API_KEY,
        model_name=model_name,
        temperature=temperature,
    )



def get_response_chain():
    logger.info("Response chain")
    model = get_chat_model()
    model_with_tools = model.bind_tools(tool_node)

    system_message = SYSTEM_PROMPT
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system",system_message),
            MessagesPlaceholder(variable_name="messages"),
        ],
        template_format="jinja2"
    )
    print(prompt)

    return prompt | model_with_tools

def get_conversation_summary_chain(summary:str =""):
    logger.info("Conversation Summary chain")
    model = get_chat_model(model_name = settings.GROQ_LLM_MODEL_CONTEXT_SUMMARY)
    

    summary_message = EXTEND_CONTEXT_SUMMARY_PROMPT if summary else CONTEXT_SUMMARY_PROMPT

    prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="messages"),
            ("human",summary_message)
        ],
        template_format="jinja2"
    )

    return prompt | model   

def get_context_summary_chain():
    logger.info("Retriever Summary chain")
    model = get_chat_model(model_name=settings.GROQ_LLM_MODEL_CONTEXT_SUMMARY)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("human", CONTEXT_SUMMARY_PROMPT),
        ],
        template_format="jinja2",
    )

    return prompt | model


