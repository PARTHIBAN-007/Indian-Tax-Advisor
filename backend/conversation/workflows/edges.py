from langgraph.graph import END
from backend.config import settings
from state import AdvisorState
def should_summarize_conversation(state: AdvisorState):
    messages = state['messages']

    if len(messages)>settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
        return "sumarization_conversation_node"
    return END