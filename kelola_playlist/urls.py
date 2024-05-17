from django.urls import path
from kelola_playlist.views import *

urlpatterns = [
    path('add_playlist/', add_playlist, name='add_playlist'),
    path('playlist_detail/', playlist_detail, name='playlist_detail'),
    path('tambah_lagu_ke_playlist/', tambah_lagu_ke_playlist, name='tambah_lagu_ke_playlist')
]