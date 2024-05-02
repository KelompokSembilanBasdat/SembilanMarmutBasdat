from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_downloaded_song, name='show_downloaded_song'),
]
