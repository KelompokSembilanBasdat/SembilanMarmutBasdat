from django.urls import path
from cek_royalti.views import cek_royalti

urlpatterns = [
    path('cek-royalti/<uuid:artist_id>/', cek_royalti, name='cek_royalti'),
]