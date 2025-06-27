# collect_books.py
import requests
import json
import time
import random
import os
from config import GOOGLE_API_KEY

# Configuration
OUTPUT_JSON_PATH = "data/raw"
OUTPUT_JSON = "books.json"
START_YEAR = 2015
END_YEAR = 2025
BASE_BOOKS = 5
YEARLY_INCREMENT = 1
MAX_RETRIES = 3
BASE_DELAY = 1.8

# Revised subject weights for better balance
SUBJECT_WEIGHTS = {
    # Nonfiction subjects with boosted weights
    "science": 3,
    "technology": 3,
    "history": 3,
    "biography": 2,
    "business": 2,
    # Fiction with reduced weight
    "fiction": 1,
    "literature": 1  
}

def get_weighted_subjects():
    """Generate subjects according to weights"""
    subjects = []
    for subject, weight in SUBJECT_WEIGHTS.items():
        subjects.extend([subject] * weight)
    return subjects

SUBJECTS = get_weighted_subjects()

def search_books(query, start_index=0):
    """Search with subject-aware querying"""
    params = {
        "q": f"{query} isbn",
        "startIndex": start_index,
        "maxResults": 20,
        "key": GOOGLE_API_KEY,
        "printType": "books",
        "langRestrict": "en",
        "fields": "items(id,volumeInfo(title,authors,publisher,publishedDate,"
                "description,industryIdentifiers,categories,imageLinks/thumbnail))"
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            time.sleep(BASE_DELAY * (1 + random.random() * 0.5))
            response = requests.get(
                "https://www.googleapis.com/books/v1/volumes",
                params=params,
                timeout=15
            )
            
            if response.status_code == 429:
                time.sleep((attempt + 1) * 5)
                continue
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException:
            time.sleep((attempt + 1) * 2)
    
    return None

def get_books_for_year(year, target_count):
    """Collection with subject balancing"""
    collected = []
    seen_ids = set()
    
    # Track subject performance
    subject_stats = {s: 0 for s in SUBJECT_WEIGHTS.keys()}
    
    while len(collected) < target_count:
        # Choose subject based on weights and past performance
        subject = random.choices(
            population=list(SUBJECT_WEIGHTS.keys()),
            weights=[max(1, SUBJECT_WEIGHTS[s] - subject_stats[s]) for s in SUBJECT_WEIGHTS],
            k=1
        )[0]
        
        queries = [
            f"subject:{subject} pub:{year}",
            f"inauthor:* subject:{subject} pub:{year}",
            f"{subject} pub:{year}"
        ]
        
        for query in queries:
            if len(collected) >= target_count:
                break
                
            data = search_books(query)
            if not data or "items" not in data:
                continue
                
            for item in data["items"]:
                book_id = item.get("id")
                if not book_id or book_id in seen_ids:
                    continue
                    
                # Verify ISBNs
                ids = item.get("volumeInfo", {}).get("industryIdentifiers", [])
                if not any(id.get("type") in ["ISBN_10", "ISBN_13"] for id in ids):
                    continue
                
                collected.append(item)
                seen_ids.add(book_id)
                subject_stats[subject] += 1
                
                if len(collected) >= target_count:
                    break
    
    # Print subject distribution
    print("  Subject distribution:")
    for subj, count in subject_stats.items():
        if count > 0:
            print(f"    {subj}: {count}")
    
    return collected[:target_count]

def main():
    print(f"Balanced Book Collection ({START_YEAR}-{END_YEAR})")
    os.makedirs(OUTPUT_JSON_PATH, exist_ok=True)
    
    results = {}
    for year in range(START_YEAR, END_YEAR + 1):
        target = BASE_BOOKS + (year - START_YEAR) * YEARLY_INCREMENT
        print(f"\nYear {year} [Target: {target} books]")
        
        books = get_books_for_year(year, target)
        results[str(year)] = books
        
        # Analyze fiction vs nonfiction
        fiction = sum(1 for b in books if "fiction" in [c.lower() for c in b.get("volumeInfo", {}).get("categories", [])])
        print(f"  Fiction: {fiction}, Nonfiction: {len(books)-fiction}")
    
    with open(os.path.join(OUTPUT_JSON_PATH, OUTPUT_JSON), 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
