from django.http import JsonResponse
from django.db.models import Avg, Count
from .models import GraphModel
import numpy as np

def generate_graphs_data(request):
    data = GraphModel.objects.all()

    # Bar chart data
    bar_data = {
        'labels': ['CHW In', 'CHW Out', 'COW In', 'COW Out'],
        'datasets': [{
            'label': 'Average Temperatures',
            'data': [
                data.aggregate(Avg('chw_in_temp'))['chw_in_temp__avg'],
                data.aggregate(Avg('chw_out_temp'))['chw_out_temp__avg'],
                data.aggregate(Avg('cow_in_temp'))['cow_in_temp__avg'],
                data.aggregate(Avg('cow_out_temp'))['cow_out_temp__avg']
            ],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)'
            ],
        }]
    }

    # Line chart data
    line_data = {
        'labels': list(data.values_list('id', flat=True)),
        'datasets': [
            {'label': 'CHW In', 'data': list(data.values_list('chw_in_temp', flat=True)), 'borderColor': 'rgb(255, 99, 132)'},
            {'label': 'CHW Out', 'data': list(data.values_list('chw_out_temp', flat=True)), 'borderColor': 'rgb(54, 162, 235)'},
            {'label': 'COW In', 'data': list(data.values_list('cow_in_temp', flat=True)), 'borderColor': 'rgb(255, 206, 86)'},
            {'label': 'COW Out', 'data': list(data.values_list('cow_out_temp', flat=True)), 'borderColor': 'rgb(75, 192, 192)'}
        ]
    }

    # Pie chart data
    temp_ranges = {
        'Low': data.filter(chw_in_temp__lt=20).count(),
        'Medium': data.filter(chw_in_temp__gte=20, chw_in_temp__lt=30).count(),
        'High': data.filter(chw_in_temp__gte=30).count()
    }
    pie_data = {
        'labels': list(temp_ranges.keys()),
        'datasets': [{
            'data': list(temp_ranges.values()),
            'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56'],
        }]
    }

    # Scatter plot data
    scatter_data = {
        'datasets': [{
            'label': 'CHW In vs COW Out',
            'data': [{'x': x, 'y': y} for x, y in zip(data.values_list('chw_in_temp', flat=True), data.values_list('cow_out_temp', flat=True))],
            'backgroundColor': 'rgba(75, 192, 192, 0.6)'
        }]
    }

    # Heatmap data
    heatmap_data = {
        'z': [
            list(data.values_list('chw_in_temp', flat=True)),
            list(data.values_list('chw_out_temp', flat=True)),
            list(data.values_list('cow_in_temp', flat=True)),
            list(data.values_list('cow_out_temp', flat=True))
        ],
        'x': list(range(len(data))),
        'y': ['CHW In', 'CHW Out', 'COW In', 'COW Out'],
    }

    # Histogram data
    histogram_data = {
        'chw_in': list(data.values_list('chw_in_temp', flat=True)),
        'chw_out': list(data.values_list('chw_out_temp', flat=True)),
        'cow_in': list(data.values_list('cow_in_temp', flat=True)),
        'cow_out': list(data.values_list('cow_out_temp', flat=True)),
    }

    # Box plot data
    box_plot_data = [
        {'y': list(data.values_list('chw_in_temp', flat=True)), 'name': 'CHW In'},
        {'y': list(data.values_list('chw_out_temp', flat=True)), 'name': 'CHW Out'},
        {'y': list(data.values_list('cow_in_temp', flat=True)), 'name': 'COW In'},
        {'y': list(data.values_list('cow_out_temp', flat=True)), 'name': 'COW Out'},
    ]

    return JsonResponse({
        'bar_chart': bar_data,
        'line_chart': line_data,
        'pie_chart': pie_data,
        'scatter_chart': scatter_data,
        'heatmap_data': heatmap_data,
        'histogram_data': histogram_data,
        'box_plot_data': box_plot_data,
    })