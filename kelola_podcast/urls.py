from django.urls import path
from . import views

urlpatterns = [
    path('podcasts/', views.podcast_management, name='podcast_management'),
    path('podcastEpisode/<uuid:podcast_id>/', views.podcast_episode_management, name='podcast_episode_management'),
    path('deletePodcasts/<uuid:podcast_id>/', views.delete_podcast, name='delete_podcast'),
    path('deleteEpisodes/<uuid:episode_id>/', views.delete_episode, name='delete_episode'),
]
