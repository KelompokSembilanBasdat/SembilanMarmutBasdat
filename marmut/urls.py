from django.contrib import admin
from django.urls import include, path

from main.views import main_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='main_page'),

    path('cek-royalti/', include('cek_royalti.urls')),
    path('downloaded-song/', include('downloaded_song.urls')),
    path('kelola-album-song/', include('kelola_album_dan_song.urls')),
    path('kelola-playlist/', include('kelola_playlist.urls')),
    path('kelola-podcast/', include('kelola_podcast.urls')),
    path('langganan-paket/', include('langganan_paket.urls')),
    path('melihat-chart/', include('melihat_chart.urls')),
    path('play-podcast/', include('play_podcast.urls')),
    path('play-song/', include('play_song.urls')),
    path('play-user-playlist/', include('play_user_playlist.urls')),
    path('searchbar/', include('searchbar.urls')),

]