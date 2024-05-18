from django.urls import path
from .views import play_podcast

urlpatterns = [
    path('podcast/<int:podcast_id>/', play_podcast, name='play_podcast'),
]
