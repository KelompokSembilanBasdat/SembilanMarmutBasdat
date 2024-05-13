from django.shortcuts import render
from utils.db import data_from_db

def show_downloaded_song(request):
    conn = data_from_db()
    cur = conn.cursor()
    cur.execute("select id_song, email_downloader from downloaded_song")
    downloaded_song = cur.fetchall()
    cur.close()
    conn.close()
    return render(request, 'downloaded_song.html',  {'downloaded_song': downloaded_song})
