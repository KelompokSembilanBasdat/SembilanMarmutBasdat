from django.urls import path
from .views import login_view, logout_view, regist_option_view, register_pengguna_view, register_label_view
from main.views import dashboard_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', regist_option_view, name='register_option'),
    path('register_pengguna/', register_pengguna_view, name='register_pengguna'),
    path('register_label/', register_label_view, name='register_label'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
