import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNKS_DIR = os.path.join(BASE_DIR, "data", "final_chunks")
VECTOR_DIR = os.path.join(BASE_DIR, "vector_store")

os.makedirs(VECTOR_DIR, exist_ok=True)

print("Loading chunks from:", CHUNKS_DIR)



def load_chunks():
    all_chunks = []

    for file in os.listdir(CHUNKS_DIR):
        if file.endswith(".json"):
            file_path = os.path.join(CHUNKS_DIR, file)

            with open(file_path, "r", encoding="utf-8") as f:
                chunks = json.load(f)
                all_chunks.extend(chunks)

    print(f"Total chunks loaded: {len(all_chunks)}")
    return all_chunks


# 🔹 Create embeddings
def create_embeddings(texts):
    print("Loading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Generating embeddings...")

    embeddings = model.encode(texts, show_progress_bar=True)

    return embeddings, model


# 🔹 Build FAISS index
def build_faiss(embeddings):
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    print("FAISS index created with", index.ntotal, "vectors")

    return index


# 🔹 Save everything
def save_vector_store(index, chunks):
    faiss.write_index(index, os.path.join(VECTOR_DIR, "index.faiss"))

    with open(os.path.join(VECTOR_DIR, "chunks_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print(" Vector store saved!")


def main():
    print("\nStarting embedding pipeline...\n")

    chunks = load_chunks()

    texts = [chunk["text"] for chunk in chunks]

    embeddings, model = create_embeddings(texts)

    index = build_faiss(embeddings)

    save_vector_store(index, chunks)

    print("\n AI search backend is ready.")


if __name__ == "__main__":
    main()