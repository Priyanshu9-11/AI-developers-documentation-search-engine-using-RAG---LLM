import os
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ✅ Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw_docs")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed_chunks")

os.makedirs(PROCESSED_DIR, exist_ok=True)

print("Reading from:", RAW_DIR)
print("Files in raw_docs:", os.listdir(RAW_DIR))
print("Saving to:", PROCESSED_DIR)


# 🔹 Chunking function
def chunk_document(text, codes, source):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_text(text)

    processed_chunks = []

    for i, chunk in enumerate(chunks):
        processed_chunks.append({
            "chunk_id": f"{source}_{i}",
            "source": source,
            "text": chunk,
            "codes": codes  # keep all codes for now (we improve later)
        })

    return processed_chunks


def main():
    print("\n🚀 Starting chunking...\n")

    total_chunks = 0

    for file in os.listdir(RAW_DIR):

        if ".json" not in file:
            continue

        print(f"\n📄 Processing file: {file}")

        file_path = os.path.join(RAW_DIR, file)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 🔥 CASE 1: LIST format
        if isinstance(data, list):

            print(f"Detected LIST with {len(data)} items")

            for doc in data:
                source = doc.get("source", "unknown")
                text = doc.get("text", "")
                codes = doc.get("codes", [])

                print(f"Source: {source}")
                print(f"Text length: {len(text)}")

                if not text.strip():
                    print("⚠️ Skipping empty text")
                    continue

                chunks = chunk_document(text, codes, source)

                print(f"Chunks created: {len(chunks)}")

                output_file = os.path.join(PROCESSED_DIR, f"{source}_chunks.json")

                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(chunks, f, indent=2)

                total_chunks += len(chunks)

        # 🔥 CASE 2: DICT format
        elif isinstance(data, dict):

            source = data.get("source", "unknown")
            text = data.get("text", "")
            codes = data.get("codes", [])

            print(f"Source: {source}")
            print(f"Text length: {len(text)}")

            if not text.strip():
                print("⚠️ Skipping empty text")
                continue

            chunks = chunk_document(text, codes, source)

            print(f"Chunks created: {len(chunks)}")

            output_file = os.path.join(PROCESSED_DIR, f"{source}_chunks.json")

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(chunks, f, indent=2)

            total_chunks += len(chunks)

        else:
            print("⚠️ Unknown format, skipping file")

    print(f"\n✅ Total chunks created: {total_chunks}")

if __name__ == "__main__":
    main()