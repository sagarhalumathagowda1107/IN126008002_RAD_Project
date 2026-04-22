from app.graph.builder import build_graph

def process_query(session_id: str, query: str):
    graph = build_graph()
    initial_state = {
        "session_id": session_id,
        "user_query": query,
        "escalation_required": False
    }
    
    result = graph.invoke(initial_state)
    return result
