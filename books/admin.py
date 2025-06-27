from django.contrib import admin

from .models import Book

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'year', 'total', 
                    'stock', 'language', 'category', 'cover_url')
    list_display_links = 'title', 
    list_editable = 'total',
    search_fields = ('title', 'author', 'isbn', 'category')
    list_per_page = 25

admin.site.register(Book, BookAdmin)