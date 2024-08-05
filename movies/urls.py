from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_movie, name='search_movie'),  # Root URL for the 'movies' app
]
