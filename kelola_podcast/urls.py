from django.urls import path
from kelola_podcast.views import *

urlpatterns = [
    path('podcast-episode-management/', podcast_management, name='podcast_management'),
    path('podcast-management/', podcast_episode_management, name='podcast_episode_management'),
]