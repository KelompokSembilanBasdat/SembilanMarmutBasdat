from django.urls import path
from main.views import dashboard_view

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
]
