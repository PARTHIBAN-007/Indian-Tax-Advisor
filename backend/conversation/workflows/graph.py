from langgraph.graph import START , END , StateGraph
from langgraph.prebuilt import tools_condition
from workflows.state import AdvisorState

from workflows.nodes import (
    conversation_node,
    summarize_conversation_node,
    summarize_context_node,
    retriever_node,
    connector_node

)
from workflows.edges import should_summarize_conversation

def create_workflow_graph():
    graph_builder = StateGraph(AdvisorState)

    graph_builder.add_node("conversation_node",conversation_node)
    graph_builder.add_node("summarization_conversation_node",summarize_conversation_node)
    graph_builder.add_node("context_summary_node",summarize_context_node)
    graph_builder.add_node("retriever_node",retriever_node)
    graph_builder.add_node("connector_node",connector_node)


    graph_builder.add_edge(START,"conversation_node")
    graph_builder.add_conditional_edges(
        "conversation_node",
        tools_condition,
        {
            "tools":"retriever_node",
            END : "connector_node",
        }
        
    )
    graph_builder.add_edge("retriever_node","summarize_context_node")
    graph_builder.add_edge("summarize_context_node","conversation_node")
    graph_builder.add_conditional_edges("connector_node", should_summarize_conversation)
    graph_builder.add_edge("summarize_conversation_node",END)

    return graph_builder



graph = create_workflow_graph().build()