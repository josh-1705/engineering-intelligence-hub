"""
Engineering Intelligence Hub — Day 2: Retrieval + Generation + UI

Takes a question, retrieves relevant chunks from the vector store built by
ingest.py, sends them to Claude for a grounded answer with citations, and
displays everything in a Streamlit chat interface.

Usage:
    streamlit run app.py

Requires:
    ANTHROPIC_API_KEY environment variable set
"""

import os

import chromadb
import ollama
import streamlit as st

# --- Config ------------------------------------------------------------

PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "supplychainx_kb"
MODEL = "llama3.1:8b"  # runs locally via Ollama, no API key or cost
TOP_K = 4  # number of chunks to retrieve per question

SYSTEM_PROMPT = """You are an engineering assistant answering questions about \
the SupplyChainX codebase, using only the provided context chunks.

Rules:
- Answer only using the given context. If the context doesn't contain the \
answer, say so clearly instead of guessing.
- Always reference which file(s) your answer comes from, using the source \
paths given with each chunk.
- Be direct and technical. This is for a developer, not a general audience.
- Keep answers concise unless the question asks for detail."""


# --- Backend logic -------------------------------------------------------

@st.cache_resource
def get_collection():
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    return client.get_collection(COLLECTION_NAME)


def retrieve_context(query: str, n_results: int = TOP_K):
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=n_results)

    chunks = []
    for i, doc in enumerate(results["documents"][0]):
        source = results["metadatas"][0][i]["source"]
        chunks.append({"text": doc, "source": source})
    return chunks


def generate_answer(query: str, chunks: list) -> str:
    context_block = "\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in chunks
    )

    user_message = f"""Context:
{context_block}

Question: {query}"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    return response["message"]["content"]


# --- Streamlit UI ----------------------------------------------------------

st.set_page_config(page_title="Engineering Intelligence Hub", page_icon="🔍")
st.title("🔍 Engineering Intelligence Hub")
st.caption("Ask questions about the SupplyChainX codebase — answers are grounded in the actual repo.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Replay chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Sources"):
                for s in msg["sources"]:
                    st.markdown(f"- `{s}`")

# New question
if question := st.chat_input("Ask something about the codebase..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving context and generating an answer..."):
            chunks = retrieve_context(question)
            answer = generate_answer(question, chunks)
            sources = sorted(set(c["source"] for c in chunks))

        st.markdown(answer)
        with st.expander("Sources"):
            for s in sources:
                st.markdown(f"- `{s}`")

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )