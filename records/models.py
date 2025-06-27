from django.db import models

from datetime import date, timedelta
from django.contrib.auth.models import User

from books.models import Book
from books.choices import status_choices


# Create your models here.

def default_due_day():
    return date.today() + timedelta(days=14)

class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    due_date = models.DateField(default=default_due_day, blank=True)
    return_date = models.DateField(null=True, blank=True)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=status_choices.items())
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ('due_date',)
        indexes = [models.Index(fields=['due_date'])]

    # def __str__(self):
    #    return self.title
