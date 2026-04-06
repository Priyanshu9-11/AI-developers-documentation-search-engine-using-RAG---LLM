import os
import json
import faiss
import numpy as np
import requests
from sentence_transformers import SentenceTransformer

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VECTOR_DIR = os.path.join(BASE_DIR, "vector_store")

INDEX_PATH = os.path.join(VECTOR_DIR, "index.faiss")
CHUNKS_PATH = os.path.join(VECTOR_DIR, "chunks_metadata.json")

print("Loading vector database...")

# Load FAISS index
index = faiss.read_index(INDEX_PATH)

# Load chunk metadata
with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Load embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

print("System Ready!\n")


# Search function
def search(query, k=2):
    query_embedding = embed_model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)

    results = []
    for idx in indices[0]:
        results.append(chunks[idx])

    return results


# Generate answer using Ollama
def generate_answer(query, results):
    context = ""

    for res in results:
        context += res["text"][:250] + "\n\n"

        if res["codes"] and len(context) < 300:
            context += "Code Example:\n"
            context += res["codes"][0][:200]

    prompt = f"""
You are an expert programming assistant.

Explain clearly and simply.
Give structured answer.
Include code example.

Context:
{context}

Question:
{query}

Answer:
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        return response.json()["response"]

    except Exception as e:
        return f"Error: {e}"


# Main loop
def main():
    while True:
        query = input("\nAsk a question (or type 'exit'): ")

        if query.lower() == "exit":
            print("Exiting...")
            break

        results = search(query)
        answer = generate_answer(query, results)

        print("\nAI Answer:\n")
        print(answer)


if __name__ == "__main__":
    main()