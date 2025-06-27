from django.shortcuts import render

from django.utils import timezone

from books.models import Book
from events.models import Event

# Create your views here.

def index(request):
    listings = Book.objects.order_by('-date_arrived')[:5]
    today = timezone.now().date()
    events = Event.objects.filter(event_date__gte=today).order_by('event_date')[:3]
    context = {"listings" : listings, "events" : events }
    return render(request, 'pages/index.html', context)

def about(request):
    return render(request, 'pages/about.html')