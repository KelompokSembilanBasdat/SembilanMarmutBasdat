from django.shortcuts import render
from django.http import Http404
from utils.db import data_from_db
from django.conf import settings

def get_podcast_details(podcast_id):
    con = data_from_db()
    cur = con.cursor()

    # Query untuk mendapatkan detail podcast berdasarkan ID
    cur.execute("""
        SELECT KONTEN.judul, KONTEN.tahun, PODCASTER.nama, SUM(EPISODE.durasi) AS total_durasi,
               KONTEN.tanggal_rilis, ARRAY_AGG(GENRE.genre) AS genres
        FROM PODCAST
        JOIN KONTEN ON PODCAST.id_konten = KONTEN.id
        JOIN PODCASTER ON PODCAST.email_podcaster = PODCASTER.email
        JOIN GENRE ON KONTEN.id = GENRE.id_konten
        JOIN EPISODE ON PODCAST.id_konten = EPISODE.id_konten_podcast
        WHERE PODCAST.id_konten = %s
        GROUP BY KONTEN.judul, KONTEN.tahun, PODCASTER.nama, KONTEN.tanggal_rilis
    """, (podcast_id,))
    podcast_details = cur.fetchone()

    cur.close()
    con.close()

    return podcast_details

def get_episode_list(podcast_id):
    con = data_from_db()
    cur = con.cursor()

    # Query untuk mendapatkan daftar episode dari suatu podcast
    cur.execute("""
        SELECT judul, deskripsi, durasi, tanggal_rilis
        FROM EPISODE
        WHERE id_konten_podcast = %s
    """, (podcast_id,))
    episode_list = cur.fetchall()

    cur.close()
    con.close()

    return episode_list

def format_duration(duration):
    hours = duration // 60
    minutes = duration % 60
    return f"{hours} jam {minutes} menit" if hours > 0 else f"{minutes} menit"

def play_podcast(request, podcast_id):
    podcast_details = get_podcast_details(podcast_id)
    episode_list = get_episode_list(podcast_id)

    if not podcast_details:
        raise Http404("Podcast not found")

    podcast_data = {
        'judul': podcast_details[0],
        'tahun': podcast_details[1],
        'podcaster': podcast_details[2],
        'total_durasi': format_duration(podcast_details[3]),
        'tanggal_rilis': podcast_details[4],
        'genres': podcast_details[5]
    }

    episodes = [
        {
            'judul': episode[0],
            'deskripsi': episode[1],
            'durasi': format_duration(episode[2]),
            'tanggal_rilis': episode[3]
        } for episode in episode_list
    ]

    return render(request, 'PlayPodcast.html', {'podcast': podcast_data, 'episodes': episodes})
