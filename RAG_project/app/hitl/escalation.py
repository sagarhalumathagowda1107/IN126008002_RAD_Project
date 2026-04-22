import json
import os
from typing import Dict, Any

TICKETS_FILE = "escalation_tickets.json"

def create_escalation_ticket(session_id: str, query: str, reason: str) -> str:
    ticket_id = f"ticket_{session_id}_{hash(query)}"
    ticket = {
        "ticket_id": ticket_id,
        "session_id": session_id,
        "query": query,
        "reason": reason,
        "status": "open",
        "human_response": ""
    }
    
    tickets = []
    if os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, "r") as f:
            tickets = json.load(f)
            
    tickets.append(ticket)
    with open(TICKETS_FILE, "w") as f:
        json.dump(tickets, f, indent=4)
        
    return ticket_id

def get_open_tickets() -> list:
    if os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, "r") as f:
            tickets = json.load(f)
        return [t for t in tickets if t["status"] == "open"]
    return []
