from django.shortcuts import render, redirect
from utils.db import data_from_db
from django.http import Http404
import uuid
from django.utils import timezone

#Untuk simpan detail podcast walaupun hanya dipakai judulnya saja
def get_podcast_details(podcast_id):
    con = data_from_db()
    cur = con.cursor()

    # Query untuk mendapatkan detail podcast berdasarkan ID
    cur.execute("""
        SELECT K.id, K.judul, array_agg(G.genre), A.nama, K.durasi, K.tanggal_rilis, K.tahun
        FROM KONTEN K
        JOIN PODCAST P ON K.id = P.id_konten
        JOIN PODCASTER Po ON P.email_podcaster = Po.email
        JOIN AKUN A ON Po.email = A.email
        JOIN GENRE G ON K.id = G.id_konten
        WHERE K.id = %s
        GROUP BY K.id, K.judul, A.nama, K.durasi, K.tanggal_rilis, K.tahun
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
        SELECT id_episode, judul, deskripsi, durasi, tanggal_rilis
        FROM EPISODE
        WHERE id_konten_podcast = %s
        ORDER BY tanggal_rilis DESC
    """, (podcast_id,))
    episode_list = cur.fetchall()

    cur.close()
    con.close()

    return episode_list

from main.views import get_user_roles

def podcast_management(request):
    con = data_from_db()
    cur = con.cursor()

    if request.method == 'POST':
        # Mendapatkan alamat email podcaster
        email = request.session.get('email')
        
        # Mendapatkan peran pengguna yang saat ini login
        roles = get_user_roles(email)
        
        # Hanya menjalankan logika jika pengguna memiliki peran podcaster
        if 'Podcaster' in roles:
            # Logika untuk membuat podcast baru
            title = request.POST.get('title')
            genre = request.POST.getlist('genre')

            # Generate random UUID
            random_id = uuid.uuid4()
            current_time = timezone.now()

            duration = 0

            # Execute SQL command with random ID
            cur.execute("""
                INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi)
                VALUES (%s, %s, %s,%s, %s)
            """, [random_id, title, current_time, current_time.year, 0])

            for g in genre:
                    cur.execute("""
                        INSERT INTO GENRE (id_konten, genre)
                        VALUES (%s, %s)
                    """, [random_id, g])

            # Menyimpan podcast dengan alamat email podcaster
            cur.execute("""
                INSERT INTO PODCAST (id_konten, email_podcaster)
                VALUES(%s, %s)
            """, [random_id, email])

            con.commit()
    
    # Logika untuk menampilkan daftar podcast
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

    return render(request, 'PodcastManagement.html', {'podcast_list': podcast_list})

def podcast_episode_management(request, podcast_id):
    podcast_details = get_podcast_details(podcast_id)
    con = data_from_db()
    cur = con.cursor()
    random_id = uuid.uuid4()
    current_time = timezone.now()

    if request.method == 'POST':
        # Ambil data dari form dan tambahkan episode baru
        title = request.POST['title']
        description = request.POST['description']
        duration = request.POST['duration']
        
        cur.execute("""
                INSERT INTO EPISODE (id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis)
                VALUES (%s, %s, %s, %s, %s, %s)  
        """, [random_id, podcast_id, title, description, duration, current_time])  

        con.commit()

    episode_list = get_episode_list(podcast_id)

    podcast_data = {
        'id': podcast_details[0],
        'judul': podcast_details[1]
    }

    episodes = [
        {
            'id': episode[0], 
            'judul': episode[1],
            'deskripsi': episode[2],
            'durasi': format_duration(episode[3]),
            'tanggal_rilis': episode[4]
        } for episode in episode_list
    ]

    cur.close()
    con.close()

    return render(request, 'PodcastEpisodeManagement.html', {'episodes': episodes, 'podcast_data': podcast_data})

def delete_podcast(request, podcast_id):
    if request.method == 'POST':
        con = data_from_db()
        cur = con.cursor()
        cur.execute("""
                DELETE FROM KONTEN
                WHERE id = %s
            """, [podcast_id])
        con.commit()
        return redirect('podcast_management')
    
def format_duration(duration):
    hours = duration // 60
    minutes = duration % 60
    return f"{hours} jam {minutes} menit" if hours > 0 else f"{minutes} menit"

def delete_episode(request, episode_id):
    con = data_from_db()
    cur = con.cursor()
    cur.execute("""
                DELETE FROM EPISODE
                WHERE id_episode = %s
            """, [episode_id])
    con.commit()
    cur.close()
    con.close()
    return redirect(request.META.get('HTTP_REFERER', 'podcast_episode_management'))


