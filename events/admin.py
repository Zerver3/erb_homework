from django.contrib import admin

from .models import Event

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'start_time', 'end_time')
    list_display_links = 'title', 
    list_editable = ('event_date', )
    search_fields = ('title', 'event_date')
    list_per_page = 25
admin.site.register(Event, EventAdmin)