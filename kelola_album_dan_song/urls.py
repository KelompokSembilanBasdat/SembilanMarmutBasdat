from django.urls import path
from kelola_album_dan_song.views import *

urlpatterns = [
    path('kelola_album_song/', kelola_album_song, name='kelola_album_song'),
    path('add_song/', add_song, name='add_song'),
    path('add_album/', add_album, name='add_album'),
    path('view_album/', view_album, name='view_album'),
]