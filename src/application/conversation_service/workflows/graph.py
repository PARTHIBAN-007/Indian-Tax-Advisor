from langgraph.graph import START , END , StateGraph
from langgraph.prebuilt import tools_condition
from application.conversation_service.workflows.state import AdvisorState
from application.conversation_service.workflows.edges import llm_tool_condition

from application.conversation_service.workflows.nodes import (
    conversation_node,
    summarize_context_node,
    retriever_node,
    web_retriever_node

)

def create_workflow_graph():
    graph_builder = StateGraph(AdvisorState)

    graph_builder.add_node("conversation_node",conversation_node)
    graph_builder.add_node("web_retriever_node",web_retriever_node)
    graph_builder.add_node("retrieve_user_context",retriever_node)
    graph_builder.add_node("summarize_context_node",summarize_context_node)
    

    graph_builder.add_edge(START,"conversation_node")
    graph_builder.add_conditional_edges(
        "conversation_node",
        llm_tool_condition,
        {
            "db_results":"retrieve_user_context",
            "web_results":"web_retriever_node",
            END : END
        }
        
    )
    
    graph_builder.add_edge("retrieve_user_context","summarize_context_node")
    graph_builder.add_edge("web_retriever_node","summarize_context_node")
    graph_builder.add_edge("summarize_context_node","conversation_node")

    return graph_builder



graph = create_workflow_graph().compile()