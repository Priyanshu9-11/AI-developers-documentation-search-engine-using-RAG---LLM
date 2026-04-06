import streamlit as st
import requests
import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_DIR = os.path.join(BASE_DIR, "vector_store")

INDEX_PATH = os.path.join(VECTOR_DIR, "index.faiss")
CHUNKS_PATH = os.path.join(VECTOR_DIR, "chunks_metadata.json")

@st.cache_resource
def load_data():
    index = faiss.read_index(INDEX_PATH)

    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    return index, chunks, model

index, chunks, embed_model = load_data()


def search(query, k=1):
    query_embedding = embed_model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)

    results = []
    for idx in indices[0]:
        results.append(chunks[idx])

    return results


def generate_answer(query, results):
    context = ""

    for res in results:
        context += res["text"][:250] + "\n\n"

        if res["codes"] and len(context) < 300:
            context += "Code Example:\n"
            context += res["codes"][0][:200] + "\n\n"

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

# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="AI Dev Assistant", layout="wide")

st.title("AI Developer Documentation Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask your question...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    with st.spinner("Thinking..."):
        results = search(user_input)
        answer = generate_answer(user_input, results)

    st.session_state.chat_history.append(("ai", answer))

# Display chat
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)