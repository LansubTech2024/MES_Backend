from django.urls import path
from . import views

urlpatterns = [
    path('charts/', views.generate_graphs, name='generate_graphs'),
]
