from django.shortcuts import render
from utils.db import data_from_db

# Create your views here.
def kelola_album_song(request):
    conn = data_from_db()
    cur = conn.cursor()
    query = """
        SELECT id_konten, id_artist, total_play, total_download
        FROM song
    """
    cur.execute(query)
    albums = cur.fetchall()
    cur.close()
    conn.close()
    return render(request, 'kelola_album_song', {'albums': albums})

def add_song(request):
    # Your logic for adding a song goes here
    return render(request, 'add_song.html') 

def add_album(request):
    # Your logic for adding an album goes here
    return render(request, 'add_album.html')

def view_album(request):
    # Your logic for viewing albums goes here
    return render(request, 'view_album.html')