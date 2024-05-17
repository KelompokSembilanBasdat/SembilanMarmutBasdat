from django.urls import path
from play_podcast.views import *

urlpatterns = [
    path('play-podcast/', play_podcast, name='play_podcast'),
]