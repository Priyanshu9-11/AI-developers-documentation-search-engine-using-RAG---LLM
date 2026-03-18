import requests
from bs4 import BeautifulSoup
import os
import json


DOC_SOURCES = {

    "python": [
        "https://docs.python.org/3/tutorial/introduction.html",
        "https://docs.python.org/3/tutorial/controlflow.html",
        "https://docs.python.org/3/tutorial/datastructures.html",
        "https://docs.python.org/3/tutorial/modules.html"
    ],

    "django": [
        "https://docs.djangoproject.com/en/stable/intro/tutorial01/",
        "https://docs.djangoproject.com/en/stable/intro/tutorial02/",
        "https://docs.djangoproject.com/en/stable/topics/http/views/",
        "https://docs.djangoproject.com/en/stable/topics/db/models/"
    ],

    "flask": [
        "https://flask.palletsprojects.com/en/latest/quickstart/",
        "https://flask.palletsprojects.com/en/latest/tutorial/",
        "https://flask.palletsprojects.com/en/latest/api/"
    ],

    "fastapi": [
        "https://fastapi.tiangolo.com/tutorial/first-steps/",
        "https://fastapi.tiangolo.com/tutorial/path-params/",
        "https://fastapi.tiangolo.com/tutorial/query-params/",
        "https://fastapi.tiangolo.com/tutorial/body/"
    ],

    "numpy": [
        "https://numpy.org/doc/stable/user/quickstart.html",
        "https://numpy.org/doc/stable/user/absolute_beginners.html"
    ],

    "pandas": [
        "https://pandas.pydata.org/docs/getting_started/intro_tutorials/01_table_oriented.html",
        "https://pandas.pydata.org/docs/getting_started/intro_tutorials/02_read_write.html"
    ]
}

# ✅ Correct project-based path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "raw_docs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Saving files to:", OUTPUT_DIR)


# 🔹 Function to scrape a single page
def scrape_page(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)

        print(f"Scraping {url} → Status: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted tags
        for tag in soup(["script", "style"]):
            tag.decompose()

        # Extract clean text
        text = soup.get_text(separator=" ", strip=True)

        # Extract code snippets
        code_blocks = soup.find_all(["code", "pre"])

        codes = [
            code.get_text(strip=True)
            for code in code_blocks
            if len(code.get_text(strip=True)) > 20
        ]

        print(f"Extracted {len(codes)} code snippets")

        return text, codes

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return "", []


# 🔹 Main function
def main():
    print("Script started...\n")

    all_docs = []

    for name, urls in DOC_SOURCES.items():
        print(f"\n📘 Processing {name}...")

        full_text = ""
        all_codes = []

        for url in urls:
            text, codes = scrape_page(url)

            full_text += text + "\n"
            all_codes.extend(codes)

        doc_data = {
            "source": name,
            "text": full_text,
            "codes": all_codes
        }

        file_path = os.path.join(OUTPUT_DIR, f"{name}.json")

        print(f"Saving file: {file_path}")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(doc_data, f, indent=2)

        print(f"{name} → Total code snippets: {len(all_codes)}")

        all_docs.append(doc_data)

    # Save combined file
    combined_path = os.path.join(OUTPUT_DIR, "all_docs.json")

    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(all_docs, f, indent=2)

    print("\n✅ All docs scraped successfully!")


if __name__ == "__main__":
    main()