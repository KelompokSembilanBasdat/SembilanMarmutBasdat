from django.urls import path
from melihat_chart.views import *

urlpatterns = [
    path('chart/', chart, name='chart'),
    path('chart-detail/', chart_detail, name='chart_detail')
]