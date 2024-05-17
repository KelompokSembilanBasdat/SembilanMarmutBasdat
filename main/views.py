from django.shortcuts import render, redirect
from utils.db import data_from_db

def dashboard_view(request):
    if not request.session.get('email'):
        return redirect('login')

    email = request.session.get('email')

    conn = data_from_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM akun WHERE email=%s", (email,))
    user = cur.fetchone()

    roles = get_user_roles(email)
    request.session['roles'] = roles
    request.session['is_premium'] = user[7]

    is_premium = user[7] and roles != ['Pengguna Biasa']

    context = {
        'name': user[2],
        'email': user[0],
        'subscription_status': 'Premium' if is_premium else 'Non-Premium',
        'contact': None,
        'hometown': user[6],
        'gender': 'Laki-laki' if user[3] == 1 else 'Perempuan',
        'birthplace': user[4],
        'birthdate': user[5],
        'role': roles,
        'is_premium': is_premium,
    }

    if 'Pengguna Biasa' in roles:
        context['playlists'] = get_user_playlists(user[0])
    if 'Artist' in roles or 'Songwriter' in roles:
        context['songs'] = get_user_songs(user[0])
    if 'Podcaster' in roles:
        context['podcasts'] = get_user_podcasts(user[0])
    if 'Label' in roles:
        context['albums'] = get_user_albums(user[0])

    cur.close()
    conn.close()

    return render(request, 'dashboard.html', context)


def get_user_roles(email):
    conn = data_from_db()
    cur = conn.cursor()
    roles = []

    cur.execute("SELECT * FROM podcaster WHERE email=%s", (email,))
    if cur.fetchone():
        roles.append('Podcaster')

    cur.execute("SELECT * FROM artist WHERE email_akun=%s", (email,))
    if cur.fetchone():
        roles.append('Artist')

    cur.execute("SELECT * FROM songwriter WHERE email_akun=%s", (email,))
    if cur.fetchone():
        roles.append('Songwriter')

    if not roles:
        roles.append('Pengguna Biasa')

    cur.close()
    conn.close()

    return roles


def get_user_playlists(user_email):
    conn = data_from_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT judul FROM user_playlist WHERE email_pembuat=%s", (user_email,))
    playlists = cur.fetchall()
    cur.close()
    conn.close()
    return [playlist[0] for playlist in playlists]


def get_user_songs(user_email):
    conn = data_from_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT k.judul 
        FROM song s
        JOIN konten k ON s.id_konten = k.id
        JOIN artist a ON s.id_artist = a.id
        WHERE a.email_akun=%s
    """, (user_email,))
    songs = cur.fetchall()
    cur.close()
    conn.close()
    return [song[0] for song in songs]


def get_user_podcasts(user_email):
    conn = data_from_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT k.judul 
        FROM podcast p
        JOIN konten k ON p.id_konten = k.id
        WHERE p.email_podcaster=%s
    """, (user_email,))
    podcasts = cur.fetchall()
    cur.close()
    conn.close()
    return [podcast[0] for podcast in podcasts]


def get_user_albums(user_email):
    conn = data_from_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.judul 
        FROM album a
        JOIN label l ON a.id_label = l.id
        WHERE l.email=%s
    """, (user_email,))
    albums = cur.fetchall()
    cur.close()
    conn.close()
    return [album[0] for album in albums]
