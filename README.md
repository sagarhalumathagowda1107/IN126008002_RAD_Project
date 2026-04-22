Dynamic RAG-Based Customer Support Assistant
A realistic AI customer support assistant powered by LangGraph, allowing users to upload specific PDFs dynamically at runtime and query them seamlessly using a context-aware Retrieval-Augmented Generation (RAG) system. No fixed local PDFs; everything is dynamic and workspace-isolated.

Capabilities
Dynamic User Uploads: Upload one or multiple PDFs at runtime.
Isolated Context Sessions: Answers use only the currently active uploaded documents. ChromaDB collections are created dynamically per session ID.
LangGraph Orchestration: Robust workflow routing (Input → Route/Intent → Retrieve Context → Evaluate → Generate/Clarify/Fallback/Escalate).
Trust-Aware Generation: Fallback mechanisms prevent hallucinations outside of the uploaded contexts.
HITL Architecture: Automated requests for clarification on vague inputs and structured escalation for complex/legal/billing issues. Features a mock Human Reviewer dashboard in Streamlit.
Streamlit GUI: Interactive and easy to use.
Folder Structure
project_root/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── graph/ (LangGraph Workflow logic)
│   ├── rag/ (Ingestor, Chunker, Vectors, Retrieval)
│   ├── llm/ (Generator, Prompts)
│   ├── hitl/ (Escalation simulation)
│   ├── ui/ (Streamlit interface)
│   └── utils/
├── chroma_db/
├── .env
├── requirements.txt
└── README.md
Setup & Run
Install Requirements:
pip install -r requirements.txt
Set Environment Variables: Copy .env.example to .env and assign your GROQ_API_KEY and LANGCHAIN_API_KEY:
cp .env.example .env
Start the Application: Run the Streamlit wrapper via main script:
python app/main.py
Or directly:

streamlit run app/ui/streamlit_app.py
Sample Run Flow
Upload Documents: Start a new session. Drag Employee_Handbook.pdf into the sidebar.
Process: Click "Process & Index Documents". The system automatically cleans text, chunks, embeds with Sentence Transformers / OpenAI, and saves to a bespoke ChromaDB collection for the session.
Valid Question: Ask "What is the PTO policy?"
LangGraph Route: retrieve -> evaluate (YES sufficient) -> generate.
Outputs valid, source-cited answer.
Vague Question: Ask "Hi, I need help."
LangGraph Route: clarify.
Outputs: "Hi there! How can I assist you with your uploaded documents today?"
Unsupported Question: Ask "Who won the Super Bowl last year?"
LangGraph Route: retrieve -> evaluate (NO sufficient context).
Outputs Fallback: "I'm sorry, I don't see enough info in the uploaded documents."
Escalation Case: Ask "I'm going to sue you for billing issues."
LangGraph Route: escalate.
Outputs escalation warning and files a pending ticket in the Sidebar hits dashboard!
BY Sagar C
