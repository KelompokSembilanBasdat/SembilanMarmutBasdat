from django.urls import path
from .views import play_podcast, podcast_list

urlpatterns = [
    path('podcast/<uuid:podcast_id>/', play_podcast, name='play_podcast'),
    path('podcastList/', podcast_list, name='podcast_list')
]
