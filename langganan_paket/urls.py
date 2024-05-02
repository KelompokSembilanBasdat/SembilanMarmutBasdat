from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_paket, name='show_paket'),
    path('pembayaran/', views.pembayaran, name='pembayaran'),
]
