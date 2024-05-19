from django.urls import path
from . import views

urlpatterns = [
    path('charts/', views.daftar_chart, name='daftar_chart'),
    path('chart/<str:chart_type>/', views.detail_chart, name='detail_chart'),
]
