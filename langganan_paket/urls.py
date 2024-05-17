from django.urls import path
from langganan_paket.views import *

urlpatterns = [
    path('', show_paket, name='show_paket'),
    path('pembayaran/', pembayaran, name='pembayaran'),
]
