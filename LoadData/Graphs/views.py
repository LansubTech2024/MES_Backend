from django.http import JsonResponse
from django.db.models import Avg, Max, Min, Count
from .models import GraphModel
import numpy as np

def generate_graphs_data(request):
    data = GraphModel.objects.all()

    # Calculate total entries
    total_entries_stats = data.aggregate(
        total_entries=Count('id')
    )

    # Calculate min and max for chw_in_temp
    chw_in_temp_stats = data.aggregate(
        min_chw_in_temp=Min('chw_in_temp'),
        max_chw_in_temp=Max('chw_in_temp')
    )

    # Calculate min and max for chw_out_temp
    chw_out_temp_stats = data.aggregate(
        min_chw_out_temp=Min('chw_out_temp'),
        max_chw_out_temp=Max('chw_out_temp')
    )

    # Calculate average for both chw_in_temp and chw_out_temp
    avg_temps = data.aggregate(
        avg_chw_in_temp=Avg('chw_in_temp'),
        avg_chw_out_temp=Avg('chw_out_temp')
    )

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

    # Waterfall chart data (modified)
    avg_data = data.aggregate(
        chw_in_avg=Avg('chw_in_temp'),
        chw_out_avg=Avg('chw_out_temp'),
        cow_in_avg=Avg('cow_in_temp'),
        cow_out_avg=Avg('cow_out_temp')
    )

    waterfall_data = {
        'x': ["Initial", "CHW In", "CHW Out", "COW In", "COW Out", "Final"],
        'y': [0, 
              avg_data['chw_in_avg'], 
              avg_data['chw_out_avg'] - avg_data['chw_in_avg'],
              avg_data['cow_in_avg'] - avg_data['chw_out_avg'],
              avg_data['cow_out_avg'] - avg_data['cow_in_avg'],
              avg_data['cow_out_avg']],
        'measure': ["absolute", "relative", "relative", "relative", "relative", "total"]
    }

    # Calculate gauge meter data for pressure
    pressure_stats = data.aggregate(
        avg_pressure=Avg('vaccum_pr')  # Replace 'vacuum_pressure' with your actual pressure field name
    )

    gauge_data = {
        'value': round(pressure_stats['avg_pressure'], 2),
        'title': 'Average Pressure',
        'range': [0, 100],  # Set appropriate range based on your data
        'steps': [
            {'range': [0, 30], 'color': 'lightgreen'},
            {'range': [30, 70], 'color': 'yellow'},
            {'range': [70, 100], 'color': 'red'}
        ],
        'threshold': {
            'line': {'color': 'red', 'width': 4},
            'value': 85  # Example threshold value, adjust as needed
        }
    }

    # 3D Surface Plot Data
    surface_data = {
        'x': list(range(10)),
        'y': list(range(10)),
        'z': [[data.first().chw_in_temp + i + j for i in range(10)] for j in range(10)]
    }


    return JsonResponse({
        "total_entries": total_entries_stats,
        "chw_in_temp": chw_in_temp_stats,
        "chw_out_temp": chw_out_temp_stats,
        "avg_temps": avg_temps,
        'line_chart': line_data,
        'waterfall_chart': waterfall_data,
        'gauge_chart': gauge_data,
        'surface_chart' : surface_data
    })