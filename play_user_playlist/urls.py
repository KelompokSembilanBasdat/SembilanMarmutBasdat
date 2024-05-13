from django.urls import path
from play_user_playlist.views import *

urlpatterns = [
    path('playlist_users/', playlist_users, name='playlist_users'),
    path('play-user-playlist/', play_user_playlist, name='play_user_playlist')
]
