from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200, blank=False)
    event_date = models.DateField(blank=False)
    start_time = models.TimeField(blank=False)
    end_time = models.TimeField(blank=False)
    description = models.TextField(blank=False)

    class Meta:
        ordering = ('event_date',)
        indexes = [models.Index(fields=['event_date'])]
