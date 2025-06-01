from langgraph.graph import END
from config import settings
from application.conversation_service.workflows.state import AdvisorState
def should_summarize_conversation(state: AdvisorState):
    messages = state['messages']

    if len(messages)>settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
        return "sumarization_conversation_node"
    return END


def should_continue(state:AdvisorState):
    num_iterations = state['num_iterations']
    max_iterations = state['max_iterations']

    if num_iterations<max_iterations:
        return "conversation_node"
    return "generate_response"


def llm_tool_condtion(state:AdvisorState):
    return "db_results"