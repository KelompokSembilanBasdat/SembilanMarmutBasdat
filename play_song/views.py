from django.shortcuts import render

# Create your views here.
def play_song(request):
    return render(request, 'play_song.html')