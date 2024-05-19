from django.shortcuts import render, redirect
from utils.db import data_from_db

def podcast_management(request):
    con = data_from_db()
    cur = con.cursor()

    if request.method == 'POST':
        # Logika untuk membuat podcast baru
        title = request.POST.get('title')
        genre = request.POST.getlist('genre')
        
        # Mendapatkan UUID baru
        cur.execute("SELECT uuid_generate_v4()")
        new_uuid = cur.fetchone()[0]  # Mengambil UUID dari hasil query
        
        # Memasukkan data ke dalam database
        cur.execute("""
            INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi)
            VALUES (%s, %s, CURRENT_DATE, EXTRACT(YEAR FROM CURRENT_DATE), 0)
        """, [new_uuid, title])
        
        cur.execute("""
            INSERT INTO PODCAST (id_konten, email_podcaster)
            VALUES (%s, %s)
        """, [new_uuid, 'podcaster@example.com'])

        for g in genre:
            cur.execute("""
                INSERT INTO GENRE (id_konten, genre)
                VALUES (%s, %s)
            """, [new_uuid, g])

        con.commit()
    
    # Logika untuk menampilkan daftar podcast
    cur.execute("""
        SELECT K.judul, COUNT(E.id_episode) AS jumlah_episode, COALESCE(SUM(E.durasi), 0) AS total_durasi
        FROM KONTEN K
        JOIN PODCAST P ON K.id = P.id_konten
        LEFT JOIN EPISODE E ON K.id = E.id_konten_podcast
        GROUP BY K.id, K.judul;
    """)
    
    podcast_list = cur.fetchall()

    podcast_list = [
        {
            'judul': row[0],
            'jumlah_episode': row[1],
            'total_durasi': row[2]
        }
        for row in podcast_list
    ]

    cur.close()
    con.close()

    return render(request, 'PodcastManagement.html', {'podcast_list': podcast_list})

def podcast_detail(request, podcast_id):
    con = data_from_db()
    cur = con.cursor()

    # Fetch podcast details based on the given podcast_id
    cur.execute("""
        SELECT K.judul, STRING_AGG(DISTINCT G.genre, ', ') AS genre, A.nama, K.tanggal_rilis, K.tahun
        FROM PODCAST P
        JOIN KONTEN K ON P.id_konten = K.id
        JOIN GENRE G ON K.id = G.id_konten
        JOIN PODCASTER PDR ON P.email_podcaster = PDR.email
        JOIN AKUN A ON PDR.email = A.email
        WHERE P.id_konten = %s
        GROUP BY K.judul, A.nama, K.tanggal_rilis, K.tahun
    """, [podcast_id])
    
    podcast_detail = cur.fetchone()

    if not podcast_detail:
        return render(request, '404.html', {'error': 'Podcast not found'})

    podcast_detail = {
        'judul': podcast_detail[0],
        'genre': podcast_detail[1],
        'nama_podcaster': podcast_detail[2],
        'tanggal_rilis': podcast_detail[3],
        'tahun': podcast_detail[4]
    }

    cur.close()
    con.close()

    return render(request, 'PodcastEpisodeManagement.html', {'podcast_detail': podcast_detail})

def view_podcast(request, podcast_id):
    con = data_from_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM Podcast WHERE id = %s", (podcast_id,))
    podcast = cur.fetchone()
    # Fetch episodes for the podcast
    cur.execute("SELECT * FROM Episode WHERE podcast_id = %s", (podcast_id,))
    episodes = cur.fetchall()
    return render(request, 'PodcastEpisodeManagement.html', {'podcast': podcast, 'episodes': episodes})

def delete_podcast(request, podcast_id):
    if request.method == 'POST':
        con = data_from_db()
        cur = con.cursor()
        cur.execute("DELETE FROM Podcast WHERE id = %s", (podcast_id,))
        con.commit()
        return redirect('podcast_management')
    
def view_episode(request, podcast_id):
    con = data_from_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM Episode WHERE podcast_id = %s", (podcast_id,))
    episodes = cur.fetchall()
    
    context = {
        'episodes': episodes
    }
    return render(request, 'PodcastEpisodeManagement.html', context)

def add_episode(request, podcast_id):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        duration = request.POST['duration']
        
        con = data_from_db()
        cur = con.cursor()
        cur.execute("INSERT INTO Episode (title, description, duration, podcast_id) VALUES (%s, %s, %s, %s)",
                    (title, description, duration, podcast_id))
        con.commit()
        
        return redirect('view_episode', podcast_id=podcast_id)
    else:
        return render(request, 'PodcastEpisodeManagement.html')
    
def delete_episode(request, episode_id):
    con = data_from_db()
    cur = con.cursor()
    cur.execute("DELETE FROM Episode WHERE id = %s", (episode_id,))
    con.commit()
    return redirect(request.META.get('HTTP_REFERER', 'podcast_episode_management'))

