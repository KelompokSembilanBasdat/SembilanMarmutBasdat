from django.urls import path
from kelola_album_dan_song.views import *

urlpatterns = [
    path('add_song/', add_song, name='add_song'),
    path('kelola-album-song-add/', kelola_album_song_add, name='kelola_album_song_add'),
    path('kelola_album_song_view/', kelola_album_song_view, name='kelola_album_song_view'),
    path('kelola_album_song/', kelola_album_song, name='kelola_album_song'),
    path('kelola_album_view/', kelola_album_view, name='kelola_album_view'),
    path('kelola_album/', kelola_album, name='kelola_album'),
]