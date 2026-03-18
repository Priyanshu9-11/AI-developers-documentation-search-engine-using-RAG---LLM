import os
import json

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNKS_DIR = os.path.join(BASE_DIR, "data", "processed_chunks")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "final_chunks")

os.makedirs(OUTPUT_DIR, exist_ok=True)


#  Simple keyword-based matching
def is_relevant(chunk, code):
    chunk_words = set(chunk.lower().split())
    code_words = set(code.lower().split())

    # overlap score
    common = chunk_words.intersection(code_words)

    return len(common) > 5  # threshold


def process_file(file):
    file_path = os.path.join(CHUNKS_DIR, file)

    with open(file_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    new_chunks = []

    for chunk in chunks:
        text = chunk["text"]
        all_codes = chunk["codes"]

        relevant_codes = []

        for code in all_codes:
            if is_relevant(text, code):
                relevant_codes.append(code)

        new_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "source": chunk["source"],
            "text": text,
            "codes": relevant_codes
        })

    output_file = os.path.join(OUTPUT_DIR, file)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(new_chunks, f, indent=2)

    print(f"{file} → processed ({len(new_chunks)} chunks)")


def main():
    print("Starting smart code mapping...\n")

    for file in os.listdir(CHUNKS_DIR):
        if file.endswith(".json"):
            process_file(file)

    print("\nDone! Smart chunks ready.")


if __name__ == "__main__":
    main()