"""
Engineering Intelligence Hub — Day 1: Ingestion + Embedding

Walks the SupplyChainX repo (backend/, frontend/, docs/incidents/, README.md),
chunks the content, and stores it in a local Chroma vector store for retrieval.

Usage:
    python ingest.py --repo-path /path/to/supplychainx

Requirements:
    pip install chromadb
"""

import argparse
import os
from pathlib import Path

import chromadb

# --- Config ---------------------------------------------------------------

INCLUDE_EXTENSIONS = {".md", ".js", ".jsx", ".sol", ".json"}

EXCLUDE_DIRS = {
    "node_modules", ".git", "build", "dist", "coverage", "__pycache__",
}

EXCLUDE_FILES = {
    "package-lock.json",  # noisy, not useful for Q&A
}

CHUNK_SIZE = 1200      # characters per chunk
CHUNK_OVERLAP = 200    # overlap so context isn't cut mid-thought

COLLECTION_NAME = "supplychainx_kb"
PERSIST_DIR = "./chroma_db"


# --- Step 1: collect files -------------------------------------------------

def collect_files(root: Path) -> list[Path]:
    """Walk the repo and return all files worth ingesting."""
    collected = []
    for dirpath, dirnames, filenames in os.walk(root):
        # prune excluded directories in place so os.walk skips them
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

        for fname in filenames:
            if fname in EXCLUDE_FILES:
                continue
            ext = Path(fname).suffix
            if ext in INCLUDE_EXTENSIONS:
                collected.append(Path(dirpath) / fname)

    return collected


# --- Step 2: chunk text -----------------------------------------------------

def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks so retrieval keeps enough context."""
    if len(text) <= size:
        return [text] if text.strip() else []

    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start += size - overlap

    return chunks


# --- Step 3: build the vector index -----------------------------------------

def build_index(repo_path: str):
    root = Path(repo_path)
    if not root.exists():
        raise FileNotFoundError(f"Repo path not found: {repo_path}")

    files = collect_files(root)
    print(f"Found {len(files)} files to ingest.")

    client = chromadb.PersistentClient(path=PERSIST_DIR)
    # Recreate the collection each run so re-ingesting doesn't duplicate chunks
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(COLLECTION_NAME)

    ids, documents, metadatas = [], [], []
    chunk_counter = 0

    for file_path in files:
        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"Skipping {file_path} ({e})")
            continue

        rel_path = str(file_path.relative_to(root))
        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            chunk_counter += 1
            ids.append(f"chunk_{chunk_counter}")
            documents.append(chunk)
            metadatas.append({"source": rel_path, "chunk_index": i})

    if not documents:
        print("No content found to ingest. Check --repo-path.")
        return

    # Chroma's default embedding function (all-MiniLM-L6-v2) runs locally,
    # no API key needed for this step.
    collection.add(ids=ids, documents=documents, metadatas=metadatas)

    print(f"Ingested {len(documents)} chunks from {len(files)} files.")
    print(f"Vector store saved to: {PERSIST_DIR}")


# --- Entry point -------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest SupplyChainX repo into a vector store.")
    parser.add_argument("--repo-path", required=True, help="Path to the cloned SupplyChainX repo")
    args = parser.parse_args()

    build_index(args.repo_path)