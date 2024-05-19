from django.shortcuts import render
from django.http import Http404
from utils.db import data_from_db
from django.conf import settings

def get_podcast_details(podcast_id):
    con = data_from_db()
    cur = con.cursor()

    # Query untuk mendapatkan detail podcast berdasarkan ID
    cur.execute("""
        SELECT K.judul, array_agg(G.genre), A.nama, K.durasi, K.tanggal_rilis, K.tahun
            FROM KONTEN K
            JOIN PODCAST P ON K.id = P.id_konten
            JOIN PODCASTER Po ON P.email_podcaster = Po.email
            JOIN AKUN A ON Po.email = A.email
            JOIN GENRE G ON K.id = G.id_konten
            WHERE K.id = %s
            GROUP BY K.judul, A.nama, K.durasi, K.tanggal_rilis, K.tahun
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
        ORDER BY tanggal_rilis DESC
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
        'genres': podcast_details[1],
        'podcaster': podcast_details[2],
        'total_durasi': format_duration(podcast_details[3]),
        'tanggal_rilis': podcast_details[4],
        #'tahun_rilis': podcast_details[5] Karena data di database terlalu random saya tidak gunakan ini
        'tahun_rilis' : podcast_details[4].year
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

def podcast_list(request):
    con = data_from_db()
    cur = con.cursor()

    cur.execute("""
        SELECT K.id, K.judul, COUNT(E.id_episode) AS jumlah_episode, COALESCE(SUM(E.durasi), 0) AS total_durasi
        FROM KONTEN K
        JOIN PODCAST P ON K.id = P.id_konten
        LEFT JOIN EPISODE E ON K.id = E.id_konten_podcast
        GROUP BY K.id, K.judul;
    """)
    
    podcast_list = cur.fetchall()

    podcast_list = [
        {
            'id': row[0],              
            'judul': row[1],
            'jumlah_episode': row[2],
            'total_durasi': row[3]
        }
        for row in podcast_list
    ]

    cur.close()
    con.close()

    return render(request, 'PodcastList.html', {'podcast_list': podcast_list})
