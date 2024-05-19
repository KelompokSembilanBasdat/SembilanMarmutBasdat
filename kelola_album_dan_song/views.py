import uuid
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from utils.db import data_from_db
from datetime import date

# Create your views here.
def kelola_album_song(request):
    email = request.session.get('email')
    roles = request.session.get('roles')
    if email is None:
        return redirect('login')

    conn = data_from_db()
    cur = conn.cursor()
    query = ""
    if ("Label" in roles):
        query = f"""
            SELECT DISTINCT ALBUM.judul, ALBUM.jumlah_lagu AS total_songs, ALBUM.total_durasi AS total_duration, ALBUM.id
            FROM ALBUM
            JOIN LABEL ON ALBUM.id_label = LABEL.id
            WHERE LABEL.email = '{email}'
            ORDER BY ALBUM.judul ASC;
        """
        cur.execute(query)
        albums = cur.fetchall()
        cur.close()
        conn.close()
        return render(request, 'kelola_song_album_label.html', {'albums': albums}) 
    else:
        query = f"""
            SELECT DISTINCT ALBUM.judul, LABEL.nama, ALBUM.jumlah_lagu, ALBUM.total_durasi, ALBUM.id
            FROM ALBUM
            JOIN LABEL ON ALBUM.id_label = LABEL.id
            JOIN SONG ON SONG.id_album = ALBUM.id
            LEFT JOIN ARTIST ON SONG.id_artist = ARTIST.id
            LEFT JOIN SONGWRITER_WRITE_SONG ON SONG.id_konten = SONGWRITER_WRITE_SONG.id_song

            WHERE (ARTIST.email_akun = '{email}' OR SONGWRITER_WRITE_SONG.id_songwriter = (SELECT id FROM SONGWRITER WHERE email_akun = '{email}'))

            ORDER BY judul ASC
        """
        cur.execute(query)
        albums = cur.fetchall()
        cur.close()
        conn.close()
        return render(request, 'kelola_song_album_artist.html', {'request': request, 'albums': albums}) 

def add_album(request):
    email = request.session.get('email')
    if email is None:
        return redirect('login')
    
    context = get_add_song_album_context(request, True)

    return render(request, 'add_album.html', context)

def add_album_submit(request):
    if request.method == 'POST':
        album = request.POST.get('album')
        label = request.POST.get('label')
        song = request.POST.get('song')
        artist = request.POST.get('artist')
        songwriters = request.POST.getlist('songwriter')
        genres = request.POST.getlist('genre')
        durasi = request.POST.get('durasi')

        create_album_song(is_album=True, judul_song=song, durasi=durasi, artist=artist,
                          songwriters=songwriters, genres=genres, judul_album=album, label=label)

        return HttpResponseRedirect(reverse('kelola_album_song'))
    else:
        return HttpResponseRedirect(reverse('kelola_album_song'))

def add_song(request, id_album):
    email = request.session.get('email')
    if email is None:
        return redirect('login')
    
    context = get_add_song_album_context(request, False, id_album)
    
    return render(request, 'add_song.html', context)

def add_song_submit(request, id_album):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        artist = request.POST.get('artist')
        songwriters = request.POST.getlist('songwriter')
        genres = request.POST.getlist('genre')
        durasi = request.POST.get('durasi')
        create_album_song(judul_song=judul, durasi=durasi, artist=artist,
                          id_album=id_album, songwriters=songwriters, genres=genres)

        return HttpResponseRedirect(reverse('add_song', args=[id_album]))
    else:
        return HttpResponseRedirect(reverse('add_song', args=[id_album]))

def delete_album(request, id_album):
    email = request.session.get('email')
    if email is None:
        return redirect('login')
    
    conn = data_from_db()
    cur = conn.cursor()

    cur.execute("SELECT id_konten, judul FROM SONG JOIN KONTEN ON id_konten = id WHERE id_album = %s;", (id,))
    konten = cur.fetchall()
    konten_ids = [item[0] for item in konten]

    cur.execute("DELETE FROM SONG WHERE id_album = %s;", (id_album,))

    for konten_id in konten_ids:
        cur.execute("DELETE FROM KONTEN WHERE id = %s;", (konten_id,))

    cur.execute("DELETE FROM ALBUM WHERE id = %s;", (id_album,))

    conn.commit()

    cur.close()
    conn.close()
    
    return HttpResponseRedirect(reverse('kelola_album_song'))

def view_album(request, id_album):
    email = request.session.get('email')
    if email is None:
        return redirect('login')
    
    conn = data_from_db()
    cur = conn.cursor()
    query = f"""
            SELECT judul
            FROM ALBUM
            WHERE ALBUM.id = '{id_album}';
        """
    cur.execute(query)
    title = cur.fetchall()

    query = f"""
        SELECT KONTEN.judul, KONTEN.durasi, SONG.total_play, SONG.total_download, KONTEN.id AS konten_id, ALBUM.id AS album_id
        FROM SONG
        JOIN KONTEN ON SONG.id_konten = KONTEN.id
        JOIN ALBUM ON SONG.id_album = ALBUM.id
        WHERE ALBUM.id = '{id_album}';
    """
    cur.execute(query)
    songs = cur.fetchall()
    cur.close()
    conn.close()
    return render(request, 'view_album.html', {'request': request, 'songs': songs, 'title': title})

def delete_song(request, id_album, id_song):
    
    email = request.session.get('email')
    if email is None:
        return redirect('login')

    conn = data_from_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM SONG WHERE id_konten = %s;", (id_song,))
    cur.execute("DELETE FROM KONTEN WHERE id = %s;", (id_song,))

    conn.commit()

    cur.execute("SELECT COUNT(*) FROM SONG WHERE id_album = %s", (id_album,))
    remaining_songs = cur.fetchone()[0]

    if remaining_songs == 0:
        cur.execute("DELETE FROM ALBUM WHERE id = %s;", (id_album,))
        conn.commit()

    cur.close()
    conn.close()

    if remaining_songs == 0:
        return HttpResponseRedirect(reverse('kelola_album_song'))
    return HttpResponseRedirect(reverse('view_album', args=[id_album]))

def get_add_song_album_context(request, is_album, id_album=None):
    email = request.session.get('email')
    roles = request.session.get('roles')
    context = {}
    if (is_album):
        labels = get_labels()
        context['label_list'] = labels
    else:
        context['id_album'] = id_album
        conn = data_from_db()
        cur = conn.cursor()

        cur.execute("SELECT judul FROM ALBUM WHERE id = %s;", (id_album,))
        album = cur.fetchall()
        title = [item[0] for item in album]

        cur.close()
        conn.close()

        context['title'] = title

    is_artist = False
    is_songwriter = False
    if ("Artist" in roles):
        is_artist = True
    if ("Songwriter" in roles):  
        is_songwriter = True
    
    id_artist = None
    id_songwriter = None
    if (is_artist):
        name, id_artist = get_artist_name(email)
    if (is_songwriter):  
        name, id_songwriter = get_songwriter_name(email)

    artist_list = get_artist()
    songwriter_list, songwriter_half = get_songwriter()
    songwriter_first_half = songwriter_list[:songwriter_half]
    songwriter_second_half = songwriter_list[songwriter_half:]

    genre_list, genre_half = get_genres()
    genre_first_half, genre_second_half = genre_list[:genre_half], genre_list[genre_half:]


    temp_context = {'request': request,
                    'id_artist': id_artist,
                    'id_songwriter': id_songwriter,
                    'name': name,
                    'is_artist': is_artist, 
                    'is_songwriter': is_songwriter,
                    'artist_list': artist_list,
                    'songwriter_first_half': songwriter_first_half,
                    'songwriter_second_half': songwriter_second_half,
                    'genre_first_half': genre_first_half,
                    'genre_second_half': genre_second_half
                    }
    
    context.update(temp_context)
    
    return context;

def create_album_song(is_album=False, judul_song=None, durasi=0, artist=None, id_album=None, songwriters=[], genres=[], judul_album=None, label=None):
    """
    CREATE ALBUM and SONG straight to database.
    is_album signify that it will create an album too or not.
    """
    conn = data_from_db()
    cur = conn.cursor()

    id_konten = str(uuid.uuid4())
    today = date.today()
    tanggal = today.strftime("%Y-%m-%d")
    tahun = today.year

    if (is_album):
        id_album = str(uuid.uuid4())
        query = f"""
        INSERT INTO ALBUM (id, judul, id_label) VALUES
        ('{id_album}', '{judul_album}', '{label}');
        """
        cur.execute(query)
        
    # CREATE KONTEN
    query = f"""
        INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi) VALUES
        ('{id_konten}', '{judul_song}', '{tanggal}', '{tahun}', {durasi});
    """
    cur.execute(query)

    # CREATE SONG
    query = f"""
        INSERT INTO SONG (id_konten, id_artist, id_album) VALUES
        ('{id_konten}', '{artist}', '{id_album}');
    """
    cur.execute(query)

    # CREATE SONGWRITER_WRITE_SONG
    for songwriter in songwriters:
        query = f"""
            INSERT INTO SONGWRITER_WRITE_SONG (id_songwriter, id_song) VALUES
            ('{songwriter}', '{id_konten}');
        """
        cur.execute(query)

        # CREATE GENRE
    for genre in genres:
        query = f"""
            INSERT INTO GENRE (id_konten, genre) VALUES
            ('{id_konten}', '{genre}');
        """
        cur.execute(query)

    conn.commit()

    cur.close()
    conn.close()

def get_labels():
    conn = data_from_db()
    cur = conn.cursor()

    query = f"""
        SELECT nama, id
        FROM label
        ORDER BY nama ASC;
    """
    cur.execute(query)
    labels = cur.fetchall()

    cur.close()
    conn.close()

    return labels

def get_artist():
    conn = data_from_db()
    cur = conn.cursor()

    query = f"""
        SELECT nama, id
        FROM akun
        JOIN artist ON akun.email = artist.email_akun
        ORDER BY nama ASC;
    """
    cur.execute(query)
    artists = cur.fetchall()

    cur.close()
    conn.close()

    return artists

def get_songwriter():
    conn = data_from_db()
    cur = conn.cursor()

    query = f"""
        SELECT nama, id
        FROM akun
        JOIN songwriter ON akun.email = songwriter.email_akun
        ORDER BY nama ASC;
    """
    cur.execute(query)
    songwriters = cur.fetchall()

    cur.close()
    conn.close()

    half = get_half(songwriters)

    return songwriters, half

def get_artist_name(email):
    conn = data_from_db()
    cur = conn.cursor()

    query = f"""
        SELECT nama
        FROM AKUN
        JOIN ARTIST ON AKUN.email = ARTIST.email_akun
        WHERE email_akun = '{email}';
    """
    cur.execute(query)
    output = cur.fetchall()
    name = [item[0] for item in output][0]

    query = f"""
        SELECT id
        FROM AKUN
        JOIN ARTIST ON AKUN.email = ARTIST.email_akun
        WHERE email_akun = '{email}';
    """
    cur.execute(query)
    output = cur.fetchall()
    id = [item[0] for item in output][0]

    cur.close()
    conn.close()

    return name, id

def get_songwriter_name(email):
    conn = data_from_db()
    cur = conn.cursor()

    query = f"""
        SELECT nama
        FROM AKUN
        JOIN SONGWRITER ON AKUN.email = SONGWRITER.email_akun
        WHERE email_akun = '{email}';
    """
    cur.execute(query)
    output = cur.fetchall()
    name = [item[0] for item in output][0]

    query = f"""
        SELECT id
        FROM AKUN
        JOIN SONGWRITER ON AKUN.email = SONGWRITER.email_akun
        WHERE email_akun = '{email}';
    """
    cur.execute(query)
    output = cur.fetchall()
    id = [item[0] for item in output][0]

    cur.close()
    conn.close()

    return name, id

def get_genres():
    genres = ['Pop', 'Rock', 'Hip Hop', 'Electronic', 'R&B', 'Country', 'Jazz', 'Classical', 'Reggae', 'Indie']
    half = get_half(genres)

    return genres, half

def get_half(list):
    """Get the midpoint of a list"""
    half = len(list) // 2

    return half