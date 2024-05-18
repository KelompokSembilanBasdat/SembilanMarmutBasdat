from django.shortcuts import render
from django.http import Http404
from utils.db import data_from_db

def daftar_chart(request):
    return render(request, 'Chart.html')

def detail_chart(request, chart_type):
    con = data_from_db()
    cur = con.cursor()

    # Fetch chart details
    cur.execute("""
        SELECT C.tipe, K.judul AS title, AK.nama AS artist, K.tanggal_rilis AS release_date, S.total_play AS plays
        FROM CHART C
        JOIN PLAYLIST_SONG PS ON C.id_playlist = PS.id_playlist
        JOIN SONG S ON PS.id_song = S.id_konten
        JOIN KONTEN K ON S.id_konten = K.id
        JOIN ARTIST A ON S.id_artist = A.id
        JOIN AKUN AK ON A.email_akun = AK.email
        WHERE C.tipe = %s
        ORDER BY S.total_play DESC
        LIMIT 20;

    """, (chart_type,))
    
    lagu_list = cur.fetchall()
    
    # Convert tuples to dictionaries
    lagu_list = [
        {
            'tipe': row[0],
            'judul': row[1],
            'artist': row[2],
            'tanggal_rilis': row[3],
            'total_play': row[4]
        }
        for row in lagu_list
    ]

    return render(request, 'chartdetail{}.html'.format(chart_type.split()[0]), {'lagu_list': lagu_list})



