from django.shortcuts import render

# Create your views here.
def playlist_users(request):
    return render(request, 'playlist_users.html')

def play_user_playlist(request):
    return render(request, 'play_user_playlist.html')