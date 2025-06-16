from langgraph.graph import START , END , StateGraph
from langgraph.prebuilt import tools_condition,ToolNode
from application.conversation_service.workflows.state import AdvisorState

from application.conversation_service.workflows.nodes import (
    conversation_node,
    tool_node
)

def create_workflow_graph():
    graph_builder = StateGraph(AdvisorState)

    graph_builder.add_node("conversation_node",conversation_node)
    graph_builder.add_node("tools",tool_node)
    

    graph_builder.add_edge(START,"conversation_node")
    graph_builder.add_conditional_edges(
        "conversation_node",
        tools_condition
    )
    
    graph_builder.add_edge("tools","conversation_node")
    # graph_builder.add_edge("summarize_context_node","conversation_node")

    return graph_builder



graph = create_workflow_graph().compile()