from django.urls import path
from downloaded_song.views import show_downloaded_song

urlpatterns = [
    path('', show_downloaded_song, name='show_downloaded_song'),
]
