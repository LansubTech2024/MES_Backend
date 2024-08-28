from django.http import JsonResponse
from django.db.models import Avg, Max, Min, Count
from django.db.models.functions import TruncMonth
from .models import GraphModel
import numpy as np
from datetime import timedelta

def generate_graphs_data(request):
    data = GraphModel.objects.all().order_by('device_date')

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
        'labels': list(data.values_list('device_date', flat=True)),
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

    # Donut Chart Data
    temp_type_counts = data.aggregate(
        chw_in_count=Count('chw_in_temp'),
        chw_out_count=Count('chw_out_temp'),
        cow_in_count=Count('cow_in_temp'),
        cow_out_count=Count('cow_out_temp')
    )

    donut_data = {
        'labels': ['CHW In', 'CHW Out', 'COW In', 'COW Out'],
        'datasets': [
            {
                'data': [
                    temp_type_counts['chw_in_count'],
                    temp_type_counts['chw_out_count'],
                    temp_type_counts['cow_in_count'],
                    temp_type_counts['cow_out_count']
                ],
                'backgroundColor': ['#0b1d78', '#0069c0', '#1fe074', '#4BC0C0']
            }
        ]
    }

    # Gantt Chart Data
    gantt_data = []
    for entry in data:
        gantt_data.append({
            'Task': f'Entry {entry.id}',
            'Start': entry.device_date.strftime('%Y-%m-%d %H:%M:%S'),
            'Finish': (entry.device_date + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),
            'Resource': f'Temp: {entry.chw_in_temp:.2f}°C'
        })

    # Combination Chart Data
    monthly_data = data.annotate(month=TruncMonth('device_date')).values('month').annotate(
        avg_chw_in_temp=Avg('chw_in_temp'),
        avg_pressure=Avg('vaccum_pr')
    ).order_by('month')

    combination_data = {
        'labels': [entry['month'].strftime('%b %Y') for entry in monthly_data],
        'datasets': [
            {
                'type': 'bar',
                'label': 'Avg CHW In Temperature',
                'data': [entry['avg_chw_in_temp'] for entry in monthly_data],
                'backgroundColor': 'rgba(255, 99, 132, 0.8)',
                'yAxisID': 'y-axis-1',
            },
            {
                'type': 'line',
                'label': 'Avg Pressure',
                'data': [entry['avg_pressure'] for entry in monthly_data],
                'borderColor': 'rgba(54, 162, 235, 1)',
                'yAxisID': 'y-axis-2',
            }
        ]
    }

    return JsonResponse({
        "total_entries": total_entries_stats,
        "chw_in_temp": chw_in_temp_stats,
        "chw_out_temp": chw_out_temp_stats,
        "avg_temps": avg_temps,
        'line_chart': line_data,
        'waterfall_chart': waterfall_data,
        'gauge_chart': gauge_data,
        'donut_chart': donut_data,
        'gantt_chart': gantt_data,
        'combination_chart': combination_data,
    })