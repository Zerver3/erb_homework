from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('add', views.add, name='add'),
    path('edit', views.edit, name='edit'),
]
