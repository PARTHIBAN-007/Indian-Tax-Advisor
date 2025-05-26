from langgraph.graph import END
from api.config import settings
from state import AdvisorState
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