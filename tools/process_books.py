# process_books.py
import json
import csv
import os
import unicodedata
from datetime import datetime

INPUT_JSON_PATH = "data/raw/books.json"
OUTPUT_CSV_PATH = "data/processed"
OUTPUT_CSV = "books.csv"

def clean_field_name(field_name):
    """Remove BOM and extra quotes from field names"""
    return field_name.replace('\ufeff', '').strip('"\' ') 

def clean_text(text, max_length=5000):
    """Clean and safely truncate text fields"""
    if not isinstance(text, str):
        return ""
    
    # Normalize Unicode and remove problematic characters
    text = unicodedata.normalize('NFC', text)
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = ''.join(char for char in text if char.isprintable() or char in ' -_|:/.')
    
    # Smart truncation to preserve sentences
    if len(text) > max_length:
        truncated = text[:max_length]
        last_period = truncated.rfind('. ')
        if last_period > 0:
            text = truncated[:last_period+1] + " [truncated]"
        else:
            text = truncated + " [truncated]"
    
    return text.strip()

def process_book_data(raw_data):
    """Process raw JSON into cleaned CSV records"""
    processed_books = []
    
    for year, items in raw_data.items():
        for item in items:
            vol_info = item.get("volumeInfo", {})
            
            # Extract identifiers
            isbn_10 = ""
            isbn_13 = ""
            for id_obj in vol_info.get("industryIdentifiers", []):
                if id_obj["type"] == "ISBN_10":
                    isbn_10 = id_obj.get("identifier", "")
                elif id_obj["type"] == "ISBN_13":
                    isbn_13 = id_obj.get("identifier", "")
            
            # Build book record
            book = {
                "published_year": year,
                "title": clean_text(vol_info.get("title", "Unknown Title")),
                "authors": "|".join(clean_text(a) for a in vol_info.get("authors", ["Unknown Author"])),
                "publisher": clean_text(vol_info.get("publisher", "Unknown Publisher")),
                "language": vol_info.get("language", "en"),
                "categories": "|".join(clean_text(c) for c in vol_info.get("categories", [])),
                "isbn_10": isbn_10,
                "isbn_13": isbn_13,
                "description": clean_text(vol_info.get("description", "")),
                "thumbnail": vol_info.get("imageLinks", {}).get("thumbnail", ""),
                "id": item.get("id", ""),
                "subject_area": clean_text(item.get("_search_query", ""))
            }
            processed_books.append(book)
    
    return processed_books

def main():
    print("Processing book data with complete metadata")
    
    # Load raw data
    try:
        with open(INPUT_JSON_PATH, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found at {INPUT_JSON_PATH}")
        exit(1)
    
    # Process data
    books = process_book_data(raw_data)
    
    # Prepare output directory
    os.makedirs(OUTPUT_CSV_PATH, exist_ok=True)
    output_path = os.path.join(OUTPUT_CSV_PATH, OUTPUT_CSV)
    
    # CSV field names
    fieldnames = [
        "published_year", "title", "authors", "publisher",
        "language", "categories", "isbn_10", "isbn_13",
        "description", "thumbnail", "id", "subject_area"
    ]
    
    # Write to CSV - using utf-8 (without BOM)
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_ALL,
            delimiter=',',
            escapechar='\\'
        )
        writer.writeheader()
        writer.writerows(books)
    
    # Verify output
    with open(output_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print("\nFirst row sample:")
        print(next(reader))
    
    # Print summary
    with_descriptions = sum(1 for b in books if b["description"])
    print(f"\nProcessed {len(books)} books")
    print(f"Books with descriptions: {with_descriptions} ({with_descriptions/len(books):.1%})")
    print(f"Data saved to {output_path}")

if __name__ == "__main__":
    main()