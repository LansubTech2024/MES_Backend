from django.urls import path
from . import views

urlpatterns = [
    path('line-chart-popup/', views.line_chart_popup, name='line_chart_popup'),
    path('waterfall-chart-popup/', views.waterfall_chart_popup, name='waterfall_chart_popup'),
    path('donut-chart-popup/', views.donut_chart_popup, name='donut_chart_popup'),
    path('combination-chart-popup/', views.combination_chart_popup, name='combination_chart_popup'),
]