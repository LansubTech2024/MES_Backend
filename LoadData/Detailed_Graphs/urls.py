from django.urls import path
from .views import views

urlpatterns = [
    path('get_prediction_data/', views.get_prediction_data, name='get_prediction_data'),
    path('get_impact_data/', views.get_impact_data, name='get_impact_data'),
]

