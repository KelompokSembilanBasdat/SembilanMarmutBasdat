from django.db import connection
from django.shortcuts import render
from utils.db import data_from_db

# Create your views here.
def cek_royalti(request):
    email = request.session['email']
    conn = data_from_db()
    cur = conn.cursor()
    roles = check_roles(email);
    query = ""
    if (check_role('label', roles)):
        query = f"""
                SELECT KONTEN.judul, ALBUM.judul, SONG.total_play, SONG.total_download, ROYALTI.jumlah
                FROM SONG
                JOIN KONTEN ON SONG.id_konten = KONTEN.id
                JOIN ALBUM ON SONG.id_album = ALBUM.id
                JOIN LABEL ON ALBUM.id_label = LABEL.id
                JOIN ROYALTI ON SONG.id_konten = ROYALTI.id_song
                WHERE LABEL.email = '{email}'
                AND ROYALTI.id_pemilik_hak_cipta = (SELECT id_pemilik_hak_cipta FROM LABEL WHERE email = '{email}');
        """
    else:
         query = f"""
                SELECT KONTEN.judul, ALBUM.judul, SONG.total_play, SONG.total_download, ROYALTI.jumlah
                FROM SONG
                JOIN KONTEN ON SONG.id_konten = KONTEN.id
                JOIN ALBUM ON SONG.id_album = ALBUM.id
                JOIN ROYALTI ON SONG.id_konten = ROYALTI.id_song
                WHERE SONG.id_artist = (SELECT id FROM ARTIST WHERE email_akun = '{email}')
                AND ROYALTI.id_pemilik_hak_cipta = (SELECT id_pemilik_hak_cipta FROM ARTIST WHERE email_akun = '{email}')

                UNION

                SELECT KONTEN.judul, ALBUM.judul, SONG.total_play, SONG.total_download, ROYALTI.jumlah
                FROM SONG
                JOIN KONTEN ON SONG.id_konten = KONTEN.id
                JOIN ALBUM ON SONG.id_album = ALBUM.id
                JOIN SONGWRITER_WRITE_SONG ON SONG.id_konten = SONGWRITER_WRITE_SONG.id_song
                JOIN ROYALTI ON SONG.id_konten = ROYALTI.id_song
                WHERE SONGWRITER_WRITE_SONG.id_songwriter = (SELECT id FROM SONGWRITER WHERE email_akun = '{email}')
                AND ROYALTI.id_pemilik_hak_cipta = (SELECT id_pemilik_hak_cipta FROM SONGWRITER WHERE email_akun = '{email}');
        """

    cur.execute(query)
    royalties = cur.fetchall()
    cur.close()
    conn.close()
    return render(request, 'cek_royalti.html', {'royalties': royalties})


def check_roles(email):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM check_roles(%s)", [email])
        result = cursor.fetchone()
    return result

def check_role(role_to_check, roles_array):
    roles = {
        'artist': roles_array[0],
        'podcaster': roles_array[1],
        'songwriter': roles_array[2],
        'label': roles_array[3]
    }
    return roles.get(role_to_check, False)