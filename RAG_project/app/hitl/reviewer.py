import json
import os
from app.hitl.escalation import TICKETS_FILE

def resolve_ticket(ticket_id: str, response: str):
    if os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, "r") as f:
            tickets = json.load(f)
            
        for t in tickets:
            if t["ticket_id"] == ticket_id:
                t["status"] = "resolved"
                t["human_response"] = response
                
        with open(TICKETS_FILE, "w") as f:
            json.dump(tickets, f, indent=4)
