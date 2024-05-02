from django.urls import path
from fitur_ijo.views import *

app_name = 'fitur_ijo'

urlpatterns = [
    path('playlist_users/', playlist_users, name='playlist_users'),
    path('add_playlist/', add_playlist, name='add_playlist'),
    path('playlist_detail/', playlist_detail, name='playlist_detail'),
    path('add_song/', add_song, name='add_song'),
    path('play-song/', play_song, name='play_song'),
    path('tambah_lagu_ke_playlist/', tambah_lagu_ke_playlist, name='tambah_lagu_ke_playlist'),
    path('play-user-playlist/', play_user_playlist, name='play_user_playlist')
]