from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
import random

<<<<<<< HEAD

def get_historical_data(chart_type):
    try:
        data = TemperatureData.objects.all().values('device_date', 'chw_in_temp', 'chw_out_temp', 'cow_in_temp', 'cow_out_temp', 'vaccum_pr')
        df = pd.DataFrame(list(data))
        df['device_date'] = pd.to_datetime(df['device_date'])

        if chart_type == 'line':
            # Line Chart: Showing trends over time
            return df.to_dict(orient='records')

        elif chart_type == 'waterfall':
            # Waterfall Chart: Showing cumulative effects of temperatures
            df['temperature_effect'] = df[['chw_in_temp', 'chw_out_temp', 'cow_in_temp', 'cow_out_temp']].sum(axis=1)
            cumulative_effect = df.groupby(df['device_date'].dt.date)['temperature_effect'].sum()
            return cumulative_effect.reset_index().to_dict(orient='records')

        elif chart_type == 'gauge':
            # Gauge Meter: Showing pressure levels
            avg_pressure = df['pressure'].mean()
            return {'pressure': avg_pressure}

        elif chart_type == 'donut':
            # Donut Chart: Showing proportions of temperature readings
            avg_temps = df[['chw_in_temp', 'chw_out_temp', 'cow_in_temp', 'cow_out_temp']].mean().to_dict()
            return avg_temps

        elif chart_type == 'combination':
            # Combination Chart: Comparing temperature and pressure in one view
            df['average_temp'] = df[['chw_in_temp', 'chw_out_temp', 'cow_in_temp', 'cow_out_temp']].mean(axis=1)
            combination_data = df.groupby(df['device_date'].dt.date).mean()[['average_temp', 'pressure']]
            return combination_data.reset_index().to_dict(orient='records')

    except Exception as e:
        return {'error': str(e)}

    return df.to_dict(orient='records')


def get_predictive_data(chart_type):
    try:
        df = pd.DataFrame(get_historical_data('line'))
        df['device_date'] = pd.to_datetime(df['device_date'])
        
        predictions = {}
        future_dates = [datetime.now() + timedelta(days=i) for i in range(1, 31)]
        
        for metric in ['chw_in_temp', 'chw_out_temp', 'cow_in_temp', 'cow_out_temp', 'vaccum_pr']:
            X = df['device_date'].astype(int) // 10**9
            y = df[metric]
            
            model = LinearRegression().fit(X.values.reshape(-1, 1), y)
            future_X = pd.to_datetime(future_dates).astype(int) // 10**9
            predictions[metric] = model.predict(future_X.values.reshape(-1, 1)).tolist()
        
        if chart_type == 'line':
            return {
                'labels': [d.strftime('%Y-%m-%d') for d in future_dates],
                'datasets': [{'label': metric, 'data': values} for metric, values in predictions.items()]
            }

        elif chart_type == 'waterfall':
            temperature_effects = np.array(predictions['chw_in_temp']) + np.array(predictions['chw_out_temp']) + \
                                  np.array(predictions['cow_in_temp']) + np.array(predictions['cow_out_temp'])
            cumulative_effect = np.cumsum(temperature_effects).tolist()
            return {
                'labels': [d.strftime('%Y-%m-%d') for d in future_dates],
                'data': cumulative_effect
            }

        elif chart_type == 'gauge':
            avg_pressure_future = np.mean(predictions['pressure'])
            return {'pressure': avg_pressure_future}

        elif chart_type == 'donut':
            avg_temps_future = {
                'chw_in_temp': np.mean(predictions['chw_in_temp']),
                'chw_out_temp': np.mean(predictions['chw_out_temp']),
                'cow_in_temp': np.mean(predictions['cow_in_temp']),
                'cow_out_temp': np.mean(predictions['cow_out_temp'])
            }
            return avg_temps_future

        elif chart_type == 'combination':
            avg_temps_future = (np.array(predictions['chw_in_temp']) + np.array(predictions['chw_out_temp']) + 
                                np.array(predictions['cow_in_temp']) + np.array(predictions['cow_out_temp'])) / 4
            combination_data_future = {
                'labels': [d.strftime('%Y-%m-%d') for d in future_dates],
                'datasets': [
                    {'label': 'Average Temperature', 'data': avg_temps_future.tolist()},
                    {'label': 'Pressure', 'data': predictions['pressure']}
                ]
            }
            return combination_data_future
        
    except Exception as e:
        return {'error': str(e)}

    return predictions


def get_impact_analysis(chart_type):
    temperature_changes = np.arange(-10, 11, 1)
    impacts = {}
    
    for metric in ['chw_in_temp', 'chw_out_temp', 'cow_in_temp', 'cow_out_temp', 'pressure']:
        impacts[metric] = {
            'energy_efficiency': (-0.5 * temperature_changes).tolist(),
            'cooling_capacity': (0.3 * temperature_changes).tolist()
        }
    
    if chart_type == 'line':
        return {
            'labels': temperature_changes.tolist(),
            'datasets': [
                {'label': f'{metric} - Energy Efficiency', 'data': values['energy_efficiency']} for metric, values in impacts.items()
            ] + [
                {'label': f'{metric} - Cooling Capacity', 'data': values['cooling_capacity']} for metric, values in impacts.items()
=======
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
>>>>>>> 7a747ffe7b1f83f95edc84281ba74a301489c29b
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

<<<<<<< HEAD
    elif chart_type == 'waterfall':
        cumulative_impact = np.cumsum(np.sum([impacts[metric]['energy_efficiency'] for metric in impacts], axis=0))
        return {
            'labels': temperature_changes.tolist(),
            'data': cumulative_impact.tolist()
        }

    elif chart_type == 'gauge':
        avg_impact_on_pressure = np.mean(impacts['pressure']['energy_efficiency'])
        return {'pressure_impact': avg_impact_on_pressure}

    elif chart_type == 'donut':
        avg_energy_efficiency = {
            metric: np.mean(values['energy_efficiency']) for metric, values in impacts.items()
        }
        return avg_energy_efficiency

    elif chart_type == 'combination':
        avg_energy_efficiency = {
            metric: np.mean(values['energy_efficiency']) for metric, values in impacts.items()
        }
        avg_cooling_capacity = {
            metric: np.mean(values['cooling_capacity']) for metric, values in impacts.items()
        }
        return {'energy_efficiency': avg_energy_efficiency, 'cooling_capacity': avg_cooling_capacity}
    
    return impacts


def graph_data_view(request):
    chart_type = request.GET.get('type', 'line')

    if chart_type not in ['line', 'waterfall', 'gauge', 'donut', 'combination']:
        return JsonResponse({'error': 'Invalid chart type'}, status=400)

    data = {
        'historical': get_historical_data(chart_type),
        'predictive': get_predictive_data(chart_type),
        'impact': get_impact_analysis(chart_type)
=======
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
>>>>>>> 7a747ffe7b1f83f95edc84281ba74a301489c29b
    }

    return JsonResponse(impact_data)
