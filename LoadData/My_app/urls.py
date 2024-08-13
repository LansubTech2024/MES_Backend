from django.urls import path
from .views import ImportMachinesView

urlpatterns = [
    path('import-machines/', ImportMachinesView.as_view(), name='import-machines'),
]
