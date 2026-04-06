# AI-developers-documentation-search-engine-using-RAG---LLM

 Overview

This project is an AI-powered developer assistant that answers programming questions using official documentation.

It uses **Retrieval-Augmented Generation (RAG)** with embeddings and a local LLM to provide accurate, context-aware answers along with code snippets.

---

##  Features

-  Semantic search using FAISS
-  Multi-source documentation (Python, Django, Flask, FastAPI, NumPy, Pandas)
-  Local LLM (Ollama - Mistral/Llama3)
-  Fast responses (optimized context + retrieval)
-  ChatGPT-like UI using Streamlit
-  Code snippets included in answers

---

## Tech Stack

- Python
- FAISS (Vector DB)
- Sentence Transformers (Embeddings)
- Ollama (Local LLM)
- Streamlit (UI)
- BeautifulSoup (Scraping)

---

## Project Structure
AI-developers-documentation-search-engine/
│
├── app.py
├── ingestion/
├── embeddings/
├── data/
├── vector_store/
├── requirements.txt
└── README.md


---

##  Setup Instructions

### 1. Clone repo

```bash
git clone <your-repo-link>
cd AI-developers-documentation-search-engine
```

# Install dependencies
pip install -r requirements.txt

# Run Ollama (IMPORTANT)
ollama run mistral

# Run the app
streamlit run app.py

# Example Queries
How to define a function in Python?
What is NumPy array?
How to build API in FastAPI?


# How it Works
Scrapes documentation from multiple sources
Splits into chunks
Converts text → embeddings
Stores in FAISS vector DB
Retrieves relevant chunks
Sends context to LLM
Generates final answer


# Future Improvements
Add PDF/document upload
Improve ranking (reranker)
Add code highlighting
Deploy on cloud


# Author
Priyanshu Bilwane

