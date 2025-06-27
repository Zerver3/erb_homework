from django.contrib import admin

from .models import BorrowRecord

# Register your models here.


class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = 'user', 'book', 'status', 'due_date'
    list_display_links = 'user', 'book', 'due_date'
    list_editable = 'status',
    search_fields = 'user', 
    list_per_page = 25

admin.site.register(BorrowRecord, BorrowRecordAdmin)

