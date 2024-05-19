from django.urls import path
from .views import downloaded_songs_view, delete_downloaded_song

urlpatterns = [
    path('', downloaded_songs_view, name='downloaded_songs'),
    path('delete/<uuid:id_song>/', delete_downloaded_song, name='delete_downloaded_song'),
]