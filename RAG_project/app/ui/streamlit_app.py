import streamlit as st
import os
import uuid
from app.main import process_query
from app.rag.pdf_ingestor import ingest_pdf
from app.rag.chunker import chunk_documents
from app.rag.vector_store import add_documents_to_store, clear_session_collection
from app.config import settings
from app.hitl.escalation import get_open_tickets
from app.hitl.reviewer import resolve_ticket

st.set_page_config(page_title="Agentic Session RAG", layout="wide")

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Initialize Session State
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("📚 Session-Based Agentic RAG")
st.sidebar.markdown(f"**Session ID:** `{st.session_state.session_id}`")

# Sidebar: File Upload
st.sidebar.header("1. Upload Documents")
uploaded_files = st.sidebar.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

if st.sidebar.button("Process Documents"):
    if uploaded_files:
        with st.spinner("Ingesting and Chunking..."):
            all_chunks = []
            for file in uploaded_files:
                file_path = os.path.join(settings.UPLOAD_DIR, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.read())
                    
                docs = ingest_pdf(file_path, st.session_state.session_id)
                chunks = chunk_documents(docs)
                all_chunks.extend(chunks)
                
            add_documents_to_store(st.session_state.session_id, all_chunks)
            st.sidebar.success(f"Processed {len(uploaded_files)} files into {len(all_chunks)} chunks.")
    else:
        st.sidebar.warning("Please upload files first.")

if st.sidebar.button("Clear Session Knowledge Base"):
    clear_session_collection(st.session_state.session_id)
    st.sidebar.success("Cleared session documents!")

# Sidebar: HITL Demo
st.sidebar.header("2. HITL Reviewer Panel")
tickets = get_open_tickets()
if tickets:
    st.sidebar.warning(f"Open Tickets: {len(tickets)}")
    for ticket in tickets:
        st.sidebar.markdown(f"**Query:** {ticket['query']}")
        human_answer = st.sidebar.text_area("Your Answer", key=f"ans_{ticket['ticket_id']}")
        if st.sidebar.button("Resolve", key=f"res_{ticket['ticket_id']}"):
            resolve_ticket(ticket['ticket_id'], human_answer)
            st.sidebar.success("Resolved!")
            st.rerun()
else:
    st.sidebar.info("No open tickets.")

# Main Chat Interface
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"]:
            st.caption(f"Sources: {', '.join(msg['sources'])}")

if prompt := st.chat_input("Ask a question about your uploaded documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = process_query(st.session_state.session_id, prompt)
            
            response = result.get("final_response", "Error generating response.")
            sources = result.get("sources", [])
            
            st.markdown(response)
            if sources:
                st.caption(f"Sources: {', '.join(sources)}")
                
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response,
                "sources": sources
            })
