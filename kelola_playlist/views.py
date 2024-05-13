from django.shortcuts import render

# Create your views here.
def add_playlist(request):
    return render(request, 'add_playlist.html')

def playlist_detail(request):
    return render(request, 'playlist_detail.html')

def tambah_lagu_ke_playlist(request):
    return render(request, 'tambah_lagu_ke_playlist.html')