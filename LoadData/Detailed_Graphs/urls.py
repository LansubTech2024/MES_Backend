from django.urls import path
from .views import graph_data_view

urlpatterns = [
    path('graph-data/', graph_data_view, name='graph_data_view'),
]
