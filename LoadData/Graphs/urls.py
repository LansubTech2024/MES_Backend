from django.urls import path
from . import views

urlpatterns = [
    path('charts/', views.generate_graphs_data, name='generate_graphs_data'),
]
