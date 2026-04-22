from app.graph.state import AgentState
from app.llm.prompts import INTENT_PROMPT, QA_PROMPT, ROUTING_PROMPT
from app.llm.generator import get_llm
from app.rag.retriever import retrieve_chunks
from app.hitl.escalation import create_escalation_ticket
from app.utils.helpers import format_context
from app.utils.logger import logger

def analyze_query(state: AgentState) -> AgentState:
    logger.info(f"Analyzing query: {state['user_query']}")
    llm = get_llm()
    chain = INTENT_PROMPT | llm
    result = chain.invoke({"query": state["user_query"]})
    intent = result.content.strip().lower()
    
    return {"intent": intent, "normalized_query": state["user_query"]}

def retrieve(state: AgentState) -> AgentState:
    logger.info(f"Retrieving for session: {state['session_id']}")
    results = retrieve_chunks(state["session_id"], state["normalized_query"])
    
    retrieved_chunks = []
    retrieval_scores = []
    sources = []
    
    for doc, score in results:
        retrieved_chunks.append({
            "text": doc.page_content,
            "filename": doc.metadata.get("filename", "Unknown"),
            "page": doc.metadata.get("page", 0)
        })
        retrieval_scores.append(score)
        sources.append(doc.metadata.get("filename", "Unknown"))
        
    return {
        "retrieved_chunks": retrieved_chunks,
        "retrieval_scores": retrieval_scores,
        "sources": list(set(sources))
    }

def evaluate_context(state: AgentState) -> AgentState:
    logger.info("Evaluating context")
    llm = get_llm()
    context = format_context(state["retrieved_chunks"])
    chain = ROUTING_PROMPT | llm
    result = chain.invoke({"query": state["normalized_query"], "context": context})
    
    is_sufficient = "yes" in result.content.strip().lower()
    return {"context_sufficient": is_sufficient}

def generate_answer(state: AgentState) -> AgentState:
    logger.info("Generating answer")
    llm = get_llm()
    context = format_context(state["retrieved_chunks"])
    chain = QA_PROMPT | llm
    result = chain.invoke({"query": state["normalized_query"], "context": context})
    
    return {"final_response": result.content, "route": "answer"}

def handle_vague(state: AgentState) -> AgentState:
    logger.info("Handling vague query")
    return {
        "final_response": "Your question is a bit unclear. Could you provide more details so I can search the uploaded documents effectively?",
        "route": "clarify"
    }

def handle_fallback(state: AgentState) -> AgentState:
    logger.info("Handling fallback")
    return {
        "final_response": "I couldn't find enough information in the currently uploaded documents to answer your question accurately.",
        "route": "fallback"
    }

def escalate_to_human(state: AgentState) -> AgentState:
    logger.info("Escalating to human")
    ticket_id = create_escalation_ticket(state["session_id"], state["user_query"], state.get("escalation_reason", "Low confidence or missing context"))
    return {
        "escalation_required": True,
        "final_response": f"I've escalated your query to a human reviewer. Ticket ID: {ticket_id}",
        "route": "escalate"
    }
