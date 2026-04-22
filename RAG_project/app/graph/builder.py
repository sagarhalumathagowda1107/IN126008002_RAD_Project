from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.graph.nodes import (
    analyze_query, retrieve, evaluate_context,
    generate_answer, handle_vague, handle_fallback, escalate_to_human
)
from app.graph.routing import route_after_analysis, route_after_retrieval

def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("analyze_query", analyze_query)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("evaluate_context", evaluate_context)
    workflow.add_node("generate_answer", generate_answer)
    workflow.add_node("handle_vague", handle_vague)
    workflow.add_node("handle_fallback", handle_fallback)
    workflow.add_node("escalate_to_human", escalate_to_human)
    
    workflow.set_entry_point("analyze_query")
    
    workflow.add_conditional_edges(
        "analyze_query",
        route_after_analysis,
        {
            "retrieve": "retrieve",
            "handle_vague": "handle_vague",
            "handle_fallback": "handle_fallback"
        }
    )
    
    workflow.add_edge("retrieve", "evaluate_context")
    
    workflow.add_conditional_edges(
        "evaluate_context",
        route_after_retrieval,
        {
            "generate_answer": "generate_answer",
            "escalate_to_human": "escalate_to_human",
            "handle_fallback": "handle_fallback"
        }
    )
    
    workflow.add_edge("generate_answer", END)
    workflow.add_edge("handle_vague", END)
    workflow.add_edge("handle_fallback", END)
    workflow.add_edge("escalate_to_human", END)
    
    return workflow.compile()
