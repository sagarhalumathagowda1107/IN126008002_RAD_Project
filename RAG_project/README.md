# Agentic Session-Based RAG

## Overview
This is a session-based Retrieval-Augmented Generation application. It allows users to upload PDF documents into isolated workspaces (sessions). Questions asked by the user are routed via an intelligent LangGraph agent that can answer directly, clarify vague questions, gracefully fallback, or escalate complex queries to a Human-In-The-Loop (HITL) reviewer.

## Features
- **Session-Based Uploads**: Uploads are stored in ChromaDB collections unique to each user session.
- **LangGraph Routing**: Analyzes query intent and evaluates if the retrieved context is sufficient.
- **Human-In-The-Loop**: Escalate ambiguous queries or unanswerable questions to an external reviewer.
- **Streamlit UI**: Complete with file uploader, chat interface, and a mock HITL resolution sidebar.

## Setup
1. Create a virtual environment: `python -m venv venv`
2. Activate it and install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set your `OPENAI_API_KEY`.
4. Run the app: `streamlit run app/ui/streamlit_app.py`
