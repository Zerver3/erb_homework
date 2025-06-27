from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('search', views.search, name='search'),
    path('search_adv', views.search_adv, name="search_adv"),
    path('listing', views.listing, name='listing'),
    path('edit', views.edit, name='edit'),
    path('add', views.add, name='add'),
    path('about/<int:book_id>', views.about, name='about'),
    path('delete/<int:book_id>', views.delete, name='delete'),
    path('borrow/<int:book_id>', views.borrow, name='borrow'), 
    path('check_in/<int:book_id>', views.check_in, name='check_in'),  
]
