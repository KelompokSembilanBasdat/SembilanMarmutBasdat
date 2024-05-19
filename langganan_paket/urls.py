from django.urls import path
from .import views

urlpatterns = [
    path('', views.show_paket, name='show_paket'),
    path('pembayaran/', views.pembayaran, name='pembayaran'),
    path('laman_pembayaran/', views.laman_pembayaran_view, name='laman_pembayaran'),
    path('riwayat_transaksi/', views.riwayat_transaksi_view, name='riwayat_transaksi'),
]