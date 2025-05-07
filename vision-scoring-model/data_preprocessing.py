import json
import re
from tqdm import tqdm
from collections import defaultdict
import unicodedata
from datetime import datetime



'''
Pre process arxiv metadata dataset,
    Load data from arxiv-metadata-oai-snapshot.json
    Field Validation: Skip entries missing any of these fields: id, title, abstract, authors, authors_parsed, categories, update_date.
    Date Filtering: Retain only papers published in 2023 or later.
    Duplicate Check: Skip entries with duplicate paper ids.
    Category Filtering: Keep only valid arXiv categories (from arxiv_all_categories).
    Retain papers with at least one cs.* category (arxiv_cs_categories subset).
    Author Cleaning: Normalize author names from authors_parsed. Apply length constraints: first (≤15), middle (≤15), last (≤20) characters. Skip papers with duplicate or zero valid authors.
    LaTeX and Text Cleanup: Remove simple LaTeX commands and math environments (\command{} and $...$).
    Strip newlines and extra whitespace from title and abstract.
    Content Filtering: Accept titles with 5–12 words. Accept abstracts with 100–250 words.
'''

MAX_FIRST_LEN = 15
MAX_MIDDLE_LEN = 15
MAX_LAST_LEN = 20

# ---------- Step 0: Load and Prepare ----------
INPUT_FILE = "arxiv-metadata-oai-snapshot.json"
OUTPUT_FILE = "arxiv_data_2023.jsonl"

from config import arxiv_cs_categories, arxiv_all_categories

def clean_latex(text):
    # Simple LaTeX cleanup
    text = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})?', '', text)
    text = re.sub(r'\$.*?\$', '', text)
    return text.strip()


def clean_author_name(parsed_entry):
    # Normalize and pad the list to ensure it has at least 3 elements
    parsed_entry = (parsed_entry + ["", "", ""])[:3]
    last, first, middle = parsed_entry

    # Normalize to Unicode NFC
    first = unicodedata.normalize("NFC", first.strip())
    middle = unicodedata.normalize("NFC", middle.strip())
    last = unicodedata.normalize("NFC", last.strip())

    # Apply length constraints
    if len(first) > MAX_FIRST_LEN or len(middle) > MAX_MIDDLE_LEN or len(last) > MAX_LAST_LEN:
        return None  # Signal to drop this author

    # Join clean name
    name = f"{first} {last} {middle}".strip()
    return re.sub(r'\s+', ' ', name)

def is_valid_word_count(text, min_words, max_words):
    return min_words <= len(text.strip().split()) <= max_words

def is_valid_title_length(title, min_words, max_words):
    return min_words <= len(title.strip().split()) <= max_words

seen_ids = set()
cleaned_data = []

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    for line in tqdm(f, desc="Processing papers"):
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue  # skip bad lines

        # print("Step 1: Filter missing critical fields")
        if not all(k in entry for k in ["id", "title", "abstract", "authors", "authors_parsed", "categories", "update_date"]):
            continue
        try:
            pub_year = datetime.strptime(entry["update_date"], "%Y-%m-%d").year
        except Exception:
            continue
        
        if pub_year < 2023:
            continue

        if entry["id"] in seen_ids:
            continue
        seen_ids.add(entry["id"])

        # print("Step 2: Parse and filter categories")
        raw_cats = entry.get("categories", "")
        # Step 2a: Keep only categories in the full arXiv category list
        filtered_cats = [cat for cat in raw_cats.split() if cat in arxiv_all_categories]
        
        # Step 2b: Retain only if at least one is in the cs.* subset
        if not any(cat in arxiv_cs_categories for cat in filtered_cats):
            continue  # skip this entry
        
        entry["categories"] = filtered_cats

        author_list = []
        for a in entry.get("authors_parsed", []):
            cleaned = clean_author_name(a)
            if cleaned:
                author_list.append(cleaned)
        
        # Drop entries with duplicate or too few valid authors
        if len(set(author_list)) < len(author_list) or not author_list:
            continue
        
        entry["authors_cleaned"] = author_list

        # print("Step 5: Clean & filter text fields")
        title = clean_latex(entry["title"]).replace("\n", " ").strip()
        abstract = clean_latex(entry["abstract"]).replace("\n", " ").strip()


        if not (is_valid_title_length(title, 5, 12) and is_valid_word_count(abstract, 100, 250)):
            continue
        entry["title"] = title
        entry["abstract"] = abstract

        # Step 6: Done above in clean_latex()

        # Retain only useful fields (optional)
        cleaned_data.append({
            "id": entry["id"],
            "title": entry["title"],
            "abstract": entry["abstract"],
            "authors": entry["authors_cleaned"],
            "categories": entry["categories"],
            "update_date": entry.get("update_date")
        })

# ---------- Save cleaned data ----------
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for item in cleaned_data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')


print(f"Saved {len(cleaned_data)} cleaned entries to {OUTPUT_FILE}")
