import os, sys
import csv
from datetime import datetime
import django
from django.core.files import File
import requests
from tempfile import NamedTemporaryFile
from pathlib import Path

BOOK_CSV="./data/processed/books.csv"


BASE_DIR = Path(__file__).resolve().parent.parent  # Gets the project root directory
sys.path.append(str(BASE_DIR))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')  # Replace with your project name
django.setup()

from books.models import Book  # Replace 'your_app' with your actual app name
from books.choices import language_choices, category_choices



def download_image(image_url):
    """Helper function to download and save book cover images"""
    if not image_url:
        return None
        
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.content)
            img_temp.flush()
            return img_temp
    except Exception as e:
        print(f"Failed to download image {image_url}: {e}")
    return None

def import_books(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            try:
                # Map CSV fields to model fields
                book_data = {
                    'title': row['title'],
                    'author': row['authors'],
                    'isbn': row['isbn_13'],
                    'year': int(row['published_year']),
                    'total': 1, # int(row['totalCopies']),
                    'stock': 1, # int(row['availabeCopies']),
                    'date_arrived': datetime.now().date(),  # Or use publication date
                    'description': row['description'],
                    'language': row['language'],  # Default to English or extract from data
                    'category': row['categories'].lower(),
                }

                # Create the book instance
                book = Book(**book_data)
                
                # Handle the cover image
                image_temp = download_image(row['thumbnail'])
                if image_temp:
                    book.cover_url.save(
                        # f"{row['id']}.jpg",  # Unique filename
                        f"{row['isbn_13']}_{row['title'][:30]}.jpg",
                        File(image_temp),
                        save=True
                    )
                    image_temp.close()
                
                book.save()
                print(f"Imported book: {book.title}")
                
            except Exception as e:
                print(f"Failed to import book {row['title']}: {e}")

if __name__ == '__main__':
    import_books(BOOK_CSV)
    print("Book import completed!")