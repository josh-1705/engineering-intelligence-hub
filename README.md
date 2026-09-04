# Engineering Intelligence Hub

A developer-focused RAG (Retrieval-Augmented Generation) system that ingests technical documentation, code, and issue reports to answer engineering questions with cited sources — reducing onboarding time and troubleshooting effort.

## Problem

New engineers and even experienced ones spend significant time searching across scattered documentation, READMEs, and past issue threads to answer basic questions about a codebase. This project builds a RAG assistant that centralizes that knowledge and returns direct, source-backed answers.

## What it does

- Ingests a GitHub repository's documentation, README, source code, and issue history
- Chunks and embeds the content into a vector database
- Retrieves the most relevant chunks for a user's question
- Generates a grounded answer using a local LLM, with citations back to the source file
- Serves the assistant through a simple Streamlit chat interface

## Architecture

1. **Ingestion** — Repository content (docs, code, issues) is collected and split into chunks.
2. **Embedding & storage** — Chunks are embedded and stored in a Chroma vector database.
3. **Retrieval** — On each query, the top-k most relevant chunks are retrieved.
4. **Generation** — Retrieved chunks are passed to a local Llama 3.1 model (via Ollama), which generates a cited answer.
5. **Interface** — A Streamlit UI lets a user ask questions and see answers with sources.

## Tech stack

- **Language:** Python
- **LLM:** Llama 3.1 (8B), running locally via Ollama
- **Vector store:** Chroma
- **UI:** Streamlit
- **Data source:** SupplyChainX repository (docs, code, incident notes)

## Setup

```bash
git clone <your-repo-url>
cd engineering-intelligence-hub

# Install Ollama (ollama.com/download), then pull the model:
ollama pull llama3.1:8b

pip install -r requirements.txt
python ingest.py --repo-path /path/to/supplychainx
streamlit run app.py
```

## Example queries

- "What does the `process_payment` function do and where is it used?"
- "Why might this incident have occurred, based on past issue reports?"
- "Walk me through how a new contributor should set up this project."

## Results / impact

- Reduced time to find relevant technical context from manual search to a single query
- Answers are grounded in the actual repository — every response includes its source
- Demonstrates a full RAG pipeline: ingestion → embedding → retrieval → generation → interface

## Future improvements

- Support for multiple repositories at once
- Confidence scoring on retrieved answers
- Slack/CLI integration for in-workflow access

## Author

Joshika — Final-year B.Tech (Computer Science, Data Science)
