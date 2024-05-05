from django.shortcuts import render

def playlist_users(request):
    return render(request, 'playlist_users.html')

def add_playlist(request):
    return render(request, 'add_playlist.html')

def playlist_detail(request):
    return render(request, 'playlist_detail.html')

def add_song(request):
    return render(request, 'add_song.html')

def play_song(request):
    return render(request, 'play_song.html')

def tambah_lagu_ke_playlist(request):
    return render(request, 'tambah_lagu_ke_playlist.html')

def play_user_playlist(request):
    return render(request, 'play_user_playlist.html')