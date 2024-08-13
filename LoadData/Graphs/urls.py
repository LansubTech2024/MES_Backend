from django.urls import path
from . import views

urlpatterns = [
    path('fetch-charts/', views.fetch_all_charts, name='fetch_all_charts'),
]