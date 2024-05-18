from django.urls import path
from . import views

urlpatterns = [
    path('podcasts/', views.podcast_list, name='podcast_management'),
    path('podcasts/create/', views.create_podcast, name='create_podcast'),
    path('podcasts/<int:podcast_id>/', views.view_podcast, name='view_podcast'),
    path('podcasts/<int:podcast_id>/delete/', views.delete_podcast, name='delete_podcast'),
    path('podcasts/<int:podcast_id>/episodes/', views.view_episode, name='view_episode'),
    path('podcasts/<int:podcast_id>/episodes/add/', views.add_episode, name='add_episode'),
    path('episodes/<int:episode_id>/delete/', views.delete_episode, name='delete_episode'),
]
