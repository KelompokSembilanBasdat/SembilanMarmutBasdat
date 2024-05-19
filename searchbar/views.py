from django.shortcuts import render
from django.http import JsonResponse
from utils.db import query

def search_bar(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        search = request.GET.get('search', '')
        formatted_search = f'%{search}%'
        search_query = """
        SELECT konten.judul AS Title, 'Song' AS ContentType, akun.nama AS CreatorName, konten.id AS ID
        FROM song
        JOIN konten ON song.id_konten = konten.id
        JOIN artist ON song.id_artist = artist.id
        JOIN akun ON artist.email_akun = akun.email
        WHERE konten.judul ILIKE %s

        UNION

        SELECT konten.judul AS Title, 'Podcast' AS ContentType, akun.nama AS CreatorName, konten.id AS ID
        FROM podcast
        JOIN konten ON podcast.id_konten = konten.id
        JOIN podcaster ON podcast.email_podcaster = podcaster.email
        JOIN akun ON podcaster.email = akun.email
        WHERE konten.judul ILIKE %s

        UNION

        SELECT user_playlist.judul AS Title, 'User Playlist' AS ContentType, akun.nama AS CreatorName, user_playlist.id_user_playlist AS ID
        FROM user_playlist
        JOIN akun ON user_playlist.email_pembuat = akun.email
        WHERE user_playlist.judul ILIKE %s

        ORDER BY ContentType DESC, Title ASC;
        """
        data = query(search_query, (formatted_search, formatted_search, formatted_search))
        return JsonResponse({'results': data})
    return render(request, 'searchbar.html')