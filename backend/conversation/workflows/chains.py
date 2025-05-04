from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from backend.config import settings

from backend.domain.prompts import SYSTEM_PROMPT ,CONTEXT_SUMMARY_PROMPT,EXTEND_CONTEXT_SUMMARY_PROMPT
from backend.conversation.workflows.tools import tools
def get_chat_model(temperature: float=0.7,model_name:str = settings.GROQ_LLM_MODEL)->ChatGroq:
    return ChatGroq(
        api_key = settings.GROQ_API_KEY,
        model_name=model_name,
        temperature=temperature,
    )



def get_response_chain():
    model = get_chat_model()
    model = model.bind_tools(tools)

    system_message = SYSTEM_PROMPT
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system",system_message),
            MessagesPlaceholder(variable_name="messages"),
        ],
        template_format="jinja2"
    )

    return prompt | model

def get_conversation_summary_chain(summary:str =""):
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
    model = get_chat_model(model_name=settings.GROQ_LLM_MODEL_CONTEXT_SUMMARY)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("human", CONTEXT_SUMMARY_PROMPT.prompt),
        ],
        template_format="jinja2",
    )

    return prompt | model


