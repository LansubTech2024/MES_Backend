from django.http import JsonResponse
from .models import TemperatureData
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

def get_historical_data(graph_type):
    try:
        data = TemperatureData.objects.all().values('device_date', 'chw_in_temp', 'chw_out_temp', 'cow_in_temp', 'cow_out_temp')
        df = pd.DataFrame(list(data))
        df['device_date'] = pd.to_datetime(df['device_date'])

        if graph_type == 'bar':
            result = df.groupby(df['device_date'].dt.date).mean()
            result.index.name = 'date'
            return result.reset_index().to_dict(orient='records')

        elif graph_type == 'line':
            return df.to_dict(orient='records')

        elif graph_type == 'pie':
            return df[['chw_in_temp', 'chw_out_temp', 'cow_in_temp', 'cow_out_temp']].mean().to_dict()

        elif graph_type == 'scatter':
            return df[['chw_in_temp', 'cow_out_temp']].to_dict(orient='records')

        elif graph_type == 'histogram':
            return {col: df[col].tolist() for col in ['chw_in_temp', 'chw_out_temp', 'cow_in_temp', 'cow_out_temp']}

        elif graph_type == 'heatmap':
            df['cow_out_temp'] = pd.to_numeric(df['cow_out_temp'], errors='coerce')
            df['chw_in_temp'] = pd.to_numeric(df['chw_in_temp'], errors='coerce')
            df['device_date'] = pd.to_datetime(df['device_date'], errors='coerce')
            df.dropna(subset=['device_date', 'chw_in_temp', 'cow_out_temp'], inplace=True)
            pivot = df.pivot(index='device_date', columns='chw_in_temp', values='cow_out_temp')
            pivot = pivot.fillna(0)
            return {
                'x': pivot.columns.tolist(),
                'y': pivot.index.astype(str).tolist(),
                'z': pivot.values.tolist()
            }

        elif graph_type == 'boxplot':
            return {col: df[col].tolist() for col in ['chw_in_temp', 'chw_out_temp', 'cow_in_temp', 'cow_out_temp']}

    except Exception as e:
        return {'error': str(e)}

    return df.to_dict(orient='records')

def get_predictive_data(graph_type):
    try:
        df = pd.DataFrame(get_historical_data('line'))
        df['device_date'] = pd.to_datetime(df['device_date'])
        
        predictions = {}
        future_dates = [datetime.now() + timedelta(days=i) for i in range(1, 31)]
        
        for metric in ['chw_in_temp', 'chw_out_temp', 'cow_in_temp', 'cow_out_temp']:
            X = df['device_date'].astype(int) // 10**9
            y = df[metric]
            
            model = LinearRegression().fit(X.values.reshape(-1, 1), y)
            future_X = pd.to_datetime(future_dates).astype(int) // 10**9
            predictions[metric] = model.predict(future_X.values.reshape(-1, 1)).tolist()
        
        if graph_type == 'bar' or graph_type == 'line':
            return {
                'labels': [d.strftime('%Y-%m-%d') for d in future_dates],
                'datasets': [{'label': metric, 'data': values} for metric, values in predictions.items()]
            }

        elif graph_type == 'pie':
            return [
                {'label': metric, 'value': sum(values)}
                for metric, values in predictions.items()
            ]

        elif graph_type == 'scatter':
            return {
                'datasets': [
                    {
                        'label': metric,
                        'data': [{'x': date.strftime('%Y-%m-%d'), 'y': float(value)} for date, value in zip(future_dates, values)]
                    }
                    for metric, values in predictions.items()
                ]
            }

        elif graph_type == 'histogram':
            return {metric: values for metric, values in predictions.items()}

        elif graph_type == 'heatmap':
            predictions = {metric: [0 if pd.isna(val) else val for val in values] for metric, values in predictions.items()}
            return {
                'x': [d.strftime('%Y-%m-%d') for d in future_dates],
                'y': list(predictions.keys()),
                'z': [predictions[metric] for metric in predictions.keys()]
            }

        elif graph_type == 'boxplot':
            return {metric: values for metric, values in predictions.items()}
        
    except Exception as e:
        return {'error': str(e)}

    return predictions

def get_impact_analysis(graph_type):
    temperature_changes = np.arange(-10, 11, 1)
    impacts = {}
    
    for metric in ['chw_in_temp', 'chw_out_temp', 'cow_in_temp', 'cow_out_temp']:
        impacts[metric] = {
            'energy_efficiency': (-0.5 * temperature_changes).tolist(),
            'cooling_capacity': (0.3 * temperature_changes).tolist()
        }
    
    if graph_type == 'bar' or graph_type == 'line':
        return {
            'labels': temperature_changes.tolist(),
            'datasets': [
                {'label': f'{metric} - Energy Efficiency', 'data': values['energy_efficiency']} for metric, values in impacts.items()
            ] + [
                {'label': f'{metric} - Cooling Capacity', 'data': values['cooling_capacity']} for metric, values in impacts.items()
            ]
        }

    elif graph_type == 'pie':
        impact_data = []
        for metric, values in impacts.items():
            impact_data.extend([
                {'label': f'{metric} - Energy Efficiency', 'value': sum(values['energy_efficiency'])},
                {'label': f'{metric} - Cooling Capacity', 'value': sum(values['cooling_capacity'])}
            ])
        return impact_data

    elif graph_type == 'scatter':
        return {
            'datasets': [
                {
                    'label': f'{metric} - Energy Efficiency',
                    'data': [{'x': float(x), 'y': float(y)} for x, y in zip(temperature_changes, values['energy_efficiency'])]
                }
                for metric, values in impacts.items()
            ] + [
                {
                    'label': f'{metric} - Cooling Capacity',
                    'data': [{'x': float(x), 'y': float(y)} for x, y in zip(temperature_changes, values['cooling_capacity'])]
                }
                for metric, values in impacts.items()
            ]
        }

    elif graph_type == 'histogram':
        return {f'{metric} - {impact_type}': values for metric, impact in impacts.items() for impact_type, values in impact.items()}

    elif graph_type == 'heatmap':
        impacts = {metric: {
            'energy_efficiency': [0 if pd.isna(val) else val for val in impacts[metric]['energy_efficiency']],
            'cooling_capacity': [0 if pd.isna(val) else val for val in impacts[metric]['cooling_capacity']]
        } for metric in impacts.keys()}
        return {
            'x': temperature_changes.tolist(),
            'y': [f'{metric} - Energy Efficiency' for metric in impacts.keys()] + [f'{metric} - Cooling Capacity' for metric in impacts.keys()],
            'z': [impacts[metric]['energy_efficiency'] for metric in impacts.keys()] + [impacts[metric]['cooling_capacity'] for metric in impacts.keys()]
        }

    elif graph_type == 'boxplot':
        impact_data = {
            f'{metric} - {impact_type}': values
            for metric, impacts in impacts.items()
            for impact_type, values in impacts.items()
        }
        return impact_data
    
    return impacts

def graph_data_view(request):
    graph_type = request.GET.get('type', 'line')

    data = {
        'historical': get_historical_data(graph_type),
        'predictive': get_predictive_data(graph_type),
        'impact': get_impact_analysis(graph_type)
    }

    return JsonResponse(data)
