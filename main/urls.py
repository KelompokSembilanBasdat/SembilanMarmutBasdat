from django.urls import path
from main.views import song_list

# register, login_user, logout_user, register_label, register_pengguna, 


urlpatterns = [
    # path('', main_page, name='main_page'),
    # path('dashboard/', show_dasboard, name='show_dasboard'),


    # path('login/', login_user, name='login'),
    # path('logout/', logout_user, name='logout'),
    # path('register/', register, name='register'),
    # path('register-pengguna/', register_pengguna, name='register_pengguna'),
    # path('register-label/', register_label, name='register_label'),

    path('coba/', song_list, name='song_list'),
]