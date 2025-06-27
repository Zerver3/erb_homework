from django.shortcuts import render

from django.shortcuts import redirect, get_object_or_404
from .models import Event

# Create your views here.

def edit(request):
    return render(request, 'events/edit.html')

def add(request):
    if request.method == "POST":
        title = request.POST["title"]
        event_date = request.POST["event_date"]
        start_time = request.POST["start_time"]
        end_time = request.POST["end_time"]
        description = request.POST["description"]
        event = Event(title=title, event_date=event_date, 
                      start_time=start_time, end_time=end_time, 
                      description=description)
        event.save()

    return redirect('accounts:dashboard')


