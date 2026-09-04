"""
Sanity check for the ingested vector store.
Run this after ingest.py to confirm retrieval is working.

Usage:
    python check.py
"""

import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("supplychainx_kb")

print(f"Total chunks stored: {collection.count()}")
print()

test_queries = [
    "How does supplier verification work?",
    "Why was there a horizontal scrollbar issue?",
]

for query in test_queries:
    print(f"Query: {query}")
    print("-" * 50)
    results = collection.query(query_texts=[query], n_results=2)

    for i, doc in enumerate(results["documents"][0]):
        source = results["metadatas"][0][i]["source"]
        print(f"[{i+1}] From: {source}")
        print(doc[:300])
        print()

    print("=" * 50)
    print()
