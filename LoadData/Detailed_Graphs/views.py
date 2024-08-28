from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
import random

@require_http_methods(["POST"])
def get_prediction_data(request):
    data = json.loads(request.body)
    chart_type = data.get('chart_type')

    # This is a placeholder. You should implement your actual prediction logic here.
    if chart_type == 'line':
        prediction_data = {
            'labels': ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'],
            'datasets': [
                {'label': 'CHW In Prediction', 'data': [random.uniform(20, 30) for _ in range(5)], 'borderColor': 'rgb(255, 99, 132)'},
                {'label': 'CHW Out Prediction', 'data': [random.uniform(20, 30) for _ in range(5)], 'borderColor': 'rgb(54, 162, 235)'},
                {'label': 'COW In Prediction', 'data': [random.uniform(20, 30) for _ in range(5)], 'borderColor': 'rgb(255, 206, 86)'},
                {'label': 'COW Out Prediction', 'data': [random.uniform(20, 30) for _ in range(5)], 'borderColor': 'rgb(75, 192, 192)'}
            ]
        }
    elif chart_type == 'waterfall':
        prediction_data = {
            'x': ["Initial", "CHW In", "CHW Out", "COW In", "COW Out", "Final"],
            'y': [0] + [random.uniform(-5, 5) for _ in range(4)] + [random.uniform(20, 30)],
            'measure': ["absolute", "relative", "relative", "relative", "relative", "total"]
        }
    elif chart_type == 'gauge':
        prediction_data = {
            'value': random.uniform(0, 100),
            'title': 'Predicted Average Pressure',
            'range': [0, 100],
            'steps': [
                {'range': [0, 30], 'color': 'lightgreen'},
                {'range': [30, 70], 'color': 'yellow'},
                {'range': [70, 100], 'color': 'red'}
            ],
            'threshold': {
                'line': {'color': 'red', 'width': 4},
                'value': 85
            }
        }
    elif chart_type == 'combination':
        prediction_data = {
            'labels': ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'],
            'datasets': [
                {
                    'type': 'line',
                    'label': 'Temperature',
                    'data': [random.uniform(20, 30) for _ in range(5)],
                    'borderColor': 'rgb(255, 99, 132)',
                    'yAxisID': 'y-axis-1'
                },
                {
                    'type': 'bar',
                    'label': 'Pressure',
                    'data': [random.uniform(50, 100) for _ in range(5)],
                    'backgroundColor': 'rgb(54, 162, 235)',
                    'yAxisID': 'y-axis-2'
                }
            ],
            'options': {
                'scales': {
                    'yAxes': [
                        {
                            'type': 'linear',
                            'display': True,
                            'position': 'left',
                            'id': 'y-axis-1',
                        },
                        {
                            'type': 'linear',
                            'display': True,
                            'position': 'right',
                            'id': 'y-axis-2',
                            'gridLines': {
                                'drawOnChartArea': False
                            }
                        }
                    ]
                }
            }
        }
    else:
        return JsonResponse({'error': 'Invalid chart type'}, status=400)

    return JsonResponse(prediction_data)

@require_http_methods(["POST"])
def get_impact_data(request):
    data = json.loads(request.body)
    chart_type = data.get('chart_type')

    # This is a placeholder. You should implement your actual impact data logic here.
    impact_data = {
        'title': f'Impact Analysis for {chart_type.capitalize()} Chart',
        'description': f'This card shows the potential impacts based on the {chart_type} chart data.',
        'factors': [
            {'name': 'Energy Consumption', 'impact': random.choice(['High', 'Medium', 'Low']), 'description': 'Impact on overall energy usage'},
            {'name': 'System Efficiency', 'impact': random.choice(['High', 'Medium', 'Low']), 'description': 'Effect on the efficiency of the cooling system'},
            {'name': 'Maintenance Needs', 'impact': random.choice(['High', 'Medium', 'Low']), 'description': 'Potential increase in maintenance requirements'}
        ]
    }

    return JsonResponse(impact_data)
