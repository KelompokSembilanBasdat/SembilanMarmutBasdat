from django.shortcuts import render

# Create your views here.
def add_song(request):
    return render(request, 'add_lagu.html')

def kelola_album_song_add(request):
    return render(request, 'kelola_album_song_add.html')

def kelola_album_song_view(request):
    return render(request, 'kelola_album_song_view.html')

def kelola_album_song(request):
    return render(request, 'kelola_album_song.html')

def kelola_album_view(request):
    return render(request, 'kelola_album_view.html')

def kelola_album(request):
    return render(request, 'kelola_album.html')