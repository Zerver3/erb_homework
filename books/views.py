from django.shortcuts import render
from django.db import models


from datetime import date
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404

from django.core.paginator import Paginator
from books.models import Book
from records.models import BorrowRecord
from .choices import language_choices, category_choices, status_choices

# Create your views here.

def add(request):
    if request.method == "POST":
        title = request.POST["title"]
        author = request.POST["author"]
        # ISBN-10: ^(?:\d{9}[\dX])$      // Example: "030640615X" 
        # ISBN-13: ^(?:\d{13})$          // Example: "9780306406157" 
        isbn = request.POST["isbn"]
        year = request.POST["year"]
        total = 1 # request.POST["total"] // number of book bought
        stock = 1 # request.POST["stock"] // number of books available to borrow
        language = request.POST["language"]
        category = request.POST["category"]
        
        date_arrived = date.today()
        # description = request.POST["description"]
        # cover_url = request.POST["cover_url"]
        book = Book(title=title, author=author, isbn=isbn, year=year, total=total,
                    stock=stock, date_arrived=date_arrived,  # cover_url=cover_url, description=description,
                    language=language, category=category) 
        book.save()
    return redirect('accounts:dashboard')

def delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    
    listings = Book.objects.all()
    context = { "language_choices" : language_choices, 
                "category_choices" : category_choices, 
                'listings' : listings,
                "value" : request.GET }
    return render(request, 'books/listings.html', context)
    # return render(request, 'accounts/dashboard.html')

def borrow(request, book_id):
    # book = get_object_or_404(Book, pk=book_id)
    # record = BorrowRecord(user=request.user.id, book=book_id)
    # record.save()

    book = Book.objects.get(id=book_id)
    record = BorrowRecord.objects.create(user=request.user, book=book, status=status_choices['borrowed'])
    record.save()

    listings = Book.objects.all()
    context = {'listings' : listings }
    return render(request, 'books/listings.html', context)    

def check_in(request, book_id):
    book = Book.objects.get(id=book_id)
    record = BorrowRecord.objects.filter(user=request.user)
    record = record.filter(book=book)
    record.delete()
    return redirect('accounts:dashboard')    



def edit(request):
    context = {"language_choices" : language_choices, 
               "category_choices" : category_choices, 
               "values" : request.GET}
    return render(request, 'books/edit.html', context)

def listing(request):
    listings = Book.objects.all().order_by('title')
    if request.method == "POST":
        if 'title' in request.POST:
            title = request.POST['title']
            if title:      
                listings = listings.filter(title__icontains=title)
        if 'author' in request.POST:
            author = request.POST['author']
            if author:           
                listings = listings.filter(author__iexact=author)
        if 'isbn' in request.POST:
            isbn = request.POST['isbn']
            if isbn:
                listings = listings.filter(isbn__iexact=isbn)            
        if 'year' in request.POST:
            year = request.POST['year']
            if year:
                listings = listings.filter(year__iexact=year)
        if 'language' in request.POST:
            language = request.POST['language']
            if language:
                listings = listings.filter(language__iexact=language)
        if 'category' in request.POST:
            category = request.POST['category']
            if category:
                listings = listings.filter(category__iexact=category)  

    context = {"language_choices" : language_choices, 
               "category_choices" : category_choices, 
               'listings' : listings,
               "values" : request.POST}

    return render(request, 'books/search.html', context)

def search_adv(request):
    context = { "language_choices" : language_choices, 
                "category_choices" : category_choices, }   
    return render(request, 'books/search.html', context)

def search(request):
    query = request.GET.get('q', '').strip()  # Get search keyword
    if query:
        listings = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(category__icontains=query)
        ).distinct()
    else:   
        listings = Book.objects.order_by('title')
        if 'title' in request.GET:
            title = request.GET['title']
            if title:      
                listings = listings.filter(title__icontains=title)
        if 'author' in request.GET:
            author = request.GET['author']
            if author:
                listings = listings.filter(author__iexact=author)
        if 'isbn' in request.GET:
            isbn = request.GET['isbn']
            if isbn:
                listings = listings.filter(isbn__iexact=isbn)            
        if 'year' in request.GET:
            year = request.GET['year']
            if year:
                listings = listings.filter(year__iexact=year)
        if 'language' in request.GET:
            language = request.GET['language']
            if language:
                listings = listings.filter(language__iexact=language)
        if 'category' in request.GET:
            category = request.GET['category']
            if category:
                listings = listings.filter(category__iexact=category)    

    # listings = listings[::-1]
    paginator = Paginator(listings, 5)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = { "language_choices" : language_choices, 
                "category_choices" : category_choices,
                # "listings": listings,
                "listings" : paged_listings, 
                "values" : request.GET }       
    return render(request, 'books/listings.html', context)

def about(request, book_id):
    book = Book.objects.get(id=book_id)
    context = { "language_choices" : language_choices, 
                "category_choices" : category_choices,
                "listing": book } 
    return render(request, 'books/about.html', context)    