from django.db import models

from datetime import date
from books.choices import language_choices, category_choices


# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    year = models.IntegerField()
    total = models.PositiveIntegerField(default=1)
    stock = models.PositiveIntegerField(default=1)
    date_arrived = models.DateField(default=date.today, blank=True)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=50, choices=language_choices.items())
    category = models.CharField(max_length=50, choices=category_choices.items())
    cover_url = models.ImageField(upload_to='photos/', blank=True)


    class Meta:
        ordering = ('-year',)
        indexes = [models.Index(fields=['year'])]

    def __str__(self):
        return self.title
