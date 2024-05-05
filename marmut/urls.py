from django.contrib import admin
from django.urls import include, path

from main.views import main_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='main_page'),
    path('paket/', include('langganan_paket.urls')),
    path('downloaded-song/', include('downloaded_song.urls')),
    path('fitur_ijo/', include('fitur_ijo.urls'))
]