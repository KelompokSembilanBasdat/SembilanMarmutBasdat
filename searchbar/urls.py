from django.urls import path
from searchbar.views import search_bar

urlpatterns = [
    path('', search_bar, name='search_bar'),
    path('search_results/', search_bar, name='search_results'),
]