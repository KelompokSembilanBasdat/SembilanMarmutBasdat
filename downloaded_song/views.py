from django.shortcuts import render, redirect
from django.http import HttpResponse
from utils.db import data_from_db

def downloaded_songs_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')

    conn = data_from_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT k.judul, ak.nama, s.id_konten
        FROM downloaded_song ds
        JOIN song s ON ds.id_song = s.id_konten
        JOIN konten k ON s.id_konten = k.id
        JOIN artist a ON s.id_artist = a.id
        JOIN akun ak ON a.email_akun = ak.email
        WHERE ds.email_downloader = %s
    """, (email,))
    songs = cur.fetchall()
    cur.close()
    conn.close()

    context = {
        'songs': [{'judul': song[0], 'artist': song[1], 'id_konten': song[2]} for song in songs]
    }

    return render(request, 'downloaded_song.html', context)

def delete_downloaded_song(request, id_song):
    email = request.session.get('email')
    if not email:
        return redirect('login')

    conn = data_from_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT k.judul
            FROM konten k
            JOIN song s ON k.id = s.id_konten
            WHERE s.id_konten = %s
        """, (id_song,))
        judul_lagu = cur.fetchone()
        if not judul_lagu:
            return HttpResponse('Lagu tidak ditemukan', status=404)

        cur.execute("""
            DELETE FROM downloaded_song
            WHERE email_downloader = %s AND id_song = %s
        """, (email, id_song))
        conn.commit()

    except Exception as e:
        conn.rollback()
        return HttpResponse(f'Error: {e}', status=400)
    finally:
        cur.close()
        conn.close()

    return render(request, 'delete_confirmation.html', {'judul_lagu': judul_lagu[0]})