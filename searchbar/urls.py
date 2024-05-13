from django.urls import path
from searchbar.views import *


urlpatterns = [
    path('', show_hasil_searchbar, name='show_hasil_searchbar'),
]