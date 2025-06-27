import os, sys
import django

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # Gets the project root directory
sys.path.append(str(BASE_DIR))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')  # Replace with your project name
django.setup()


from django.contrib.auth.models import User
from books.models import Book
from records.models import BorrowRecord

BorrowRecord.objects.all().delete()
Book.objects.all().delete()
# User.objects.all().delete()



