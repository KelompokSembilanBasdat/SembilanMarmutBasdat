from django.shortcuts import render
from main.models import data_from_db

def song_list(request):
    conn = data_from_db()
    cur = conn.cursor()
    cur.execute("SELECT id_konten, id_artist, total_play, total_download FROM song")
    songs = cur.fetchall()
    cur.close()
    conn.close()
    return render(request, 'songs.html', {'songs': songs})

def main_page(request):
    return render(request, 'main.html')
