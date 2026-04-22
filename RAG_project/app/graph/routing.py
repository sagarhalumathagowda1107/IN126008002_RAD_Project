from app.graph.state import AgentState

def route_after_analysis(state: AgentState) -> str:
    if state["intent"] == "vague":
        return "handle_vague"
    elif state["intent"] == "unsupported":
        return "handle_fallback"
    else:
        return "retrieve"

def route_after_retrieval(state: AgentState) -> str:
    # If no documents retrieved at all
    if not state.get("retrieved_chunks"):
        return "handle_fallback"
    
    # Check if context is sufficient based on LLM evaluation
    if state.get("context_sufficient"):
        return "generate_answer"
    else:
        return "escalate_to_human"
