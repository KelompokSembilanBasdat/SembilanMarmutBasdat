from django.urls import path
from cek_royalti.views import cek_royalti

urlpatterns = [
    path('', cek_royalti, name='cek_royalti'),
]