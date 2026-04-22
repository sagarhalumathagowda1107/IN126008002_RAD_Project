from typing import TypedDict, List, Dict, Any, Optional
from pydantic import BaseModel

class AgentState(TypedDict):
    session_id: str
    uploaded_files: List[str]
    active_collection: str
    user_query: str
    normalized_query: str
    intent: str
    retrieved_chunks: List[Dict[str, Any]]
    retrieval_scores: List[float]
    context_sufficient: bool
    answer_draft: str
    confidence_score: float
    route: str
    escalation_required: bool
    escalation_reason: str
    human_decision: str
    final_response: str
    sources: List[str]
    error: str
