from django.urls import path
from kelola_album_dan_song.views import *

urlpatterns = [
    path('', kelola_album_song, name='kelola_album_song'),
    path('add_album/', add_album, name='add_album'),
    path('add_album_submit/', add_album_submit, name='add_album_submit'),
    path('add_song/<uuid:id_album>/', add_song, name='add_song'),
    path('add_song_submit/<uuid:id_album>/', add_song_submit, name='add_song_submit'),
    path('view_album/<uuid:id_album>/', view_album, name='view_album'),
    path('delete_album/<uuid:id_album>/', delete_album, name='delete_album'),
    path('delete_song/<uuid:id_album>/<uuid:id_song>', delete_song, name='delete_song')
]