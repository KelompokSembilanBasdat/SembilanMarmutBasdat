from django.urls import path
from play_song.views import *

urlpatterns = [
    path('play-song/', play_song, name='play_song'),
]