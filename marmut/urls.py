from django.contrib import admin
from django.urls import path, include
from main.views import main_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='main_page'),
    path('paket/', include('langganan_paket.urls')),
    path('downloaded-song/', include('downloaded_song.urls')),
]