from django.shortcuts import render
from main.models import DownloadedSong

# Create your views here.
def show_downloaded_song(request):
    downloaded_songs = DownloadedSong.objects.select_related('id_song', 'id_song__id_konten', 'id_song__id_artist', 'id_song__id_artist__email_akun').all()
    return render(request, 'downloaded_song.html', {'downloaded_songs': downloaded_songs})
