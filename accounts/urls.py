from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('delete<int:user_id>', views.delete, name='delete'),

    path('edit', views.edit, name='edit'),
    path('listing', views.listing, name='listing'),
    path('reset', views.reset, name='reset'),
    path('search', views.search, name='search'),

]
