from langchain_core.prompts import PromptTemplate

INTENT_PROMPT = PromptTemplate.from_template("""
Analyze the user's query and classify the intent into one of the following categories:
- "support": The user is asking a clear question that can likely be answered by documentation.
- "vague": The user's question is unclear, too short, or lacks context.
- "unsupported": The user is asking about something completely unrelated to any expected document, or asking for inappropriate content.

User Query: {query}

Intent (reply ONLY with "support", "vague", or "unsupported"):
""")

QA_PROMPT = PromptTemplate.from_template("""
You are a helpful and professional support assistant. Use ONLY the following retrieved context to answer the user's question.
If the answer is not contained in the context, say explicitly: "I could not find the answer to this question in the uploaded documents." Do not make up an answer.

Context:
{context}

User Question: {query}

Answer:
""")

ROUTING_PROMPT = PromptTemplate.from_template("""
You need to decide whether the provided retrieved context has enough information to answer the user's query.
User Query: {query}
Context: {context}

Reply ONLY with "yes" if there is sufficient evidence, or "no" if there is not.
""")
