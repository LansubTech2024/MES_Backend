from django.http import JsonResponse
from .models import TemperatureData
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# List of labels you want to use
labels = ['CHW_IN_TEMP', 'CHW_OUT_TEMP', 'COW_IN_TEMP', 'COW_OUT_TEMP', 'STEAM_COND_TEMP', 'HTG_TEMP', 
          'LTG_TEMP', 'HTHE_OUT_TEMP', 'SPRAY_TEMP', 'DL_SLN_TEMP', 'REF_TEMP', 'U_TUBE_TEMP', 
          'OVRFLW_LTG_TEMP', 'HTG_TOP_TEMP', 'HTG_BOT_TEMP', 'HTG_TB_ABS_DIFF_TEMP', 'VACCUM_PR', 
          'REF_TEMP_LOW_SP', 'REF_TEMP_LOW_HYS', 'HTG_PR_HI_SP', 'HTG_PR_LOW_LMT_SP', 'HTG_PR_HI_LMT_SP', 
          'HTG_PR_HI_HYS', 'HTG_VAP_TEMP', 'TIME']

def get_historical_data(graph_type):
    try:
        data = TemperatureData.objects.all().values(*[label.lower() for label in labels])
        df = pd.DataFrame(list(data))
        df['device_date'] = pd.to_datetime(df['device_date'])

        if graph_type in ['bar', 'column']:
            result = df.groupby(df['device_date'].dt.date).mean()
            result.index.name = 'date'
            return {
                'labels': result.index.astype(str).tolist(),
                'datasets': [
                    {'label': label, 'data': result[label.lower()].tolist()}
                    for label in labels if label.lower() in result.columns
                ]
            }

        elif graph_type == 'line':
            return df.to_dict(orient='records')

        elif graph_type == 'pie':
            avg_values = df[[label.lower() for label in labels]].mean()
            return [
                {'label': label, 'value': avg_values[label.lower()]}
                for label in labels if label.lower() in avg_values.index
            ]

        # Other graph types remain the same
        # ...

    except Exception as e:
        return {'error': str(e)}

    return df.to_dict(orient='records')

def get_predictive_data(graph_type):
    try:
        df = pd.DataFrame(get_historical_data('line'))
        df['device_date'] = pd.to_datetime(df['device_date'])
        
        predictions = {}
        future_dates = [datetime.now() + timedelta(days=i) for i in range(1, 31)]
        
        for label in labels:
            metric = label.lower()
            if metric in df.columns:
                X = df['device_date'].astype(int) // 10**9
                y = df[metric]
                
                model = LinearRegression().fit(X.values.reshape(-1, 1), y)
                future_X = pd.to_datetime(future_dates).astype(int) // 10**9
                predictions[metric] = model.predict(future_X.values.reshape(-1, 1)).tolist()
        
        if graph_type in ['bar', 'column', 'line']:
            return {
                'labels': [d.strftime('%Y-%m-%d') for d in future_dates],
                'datasets': [{'label': label, 'data': predictions[label.lower()]} for label in labels if label.lower() in predictions]
            }

        elif graph_type == 'pie':
            return [
                {'label': label, 'value': sum(predictions[label.lower()])}
                for label in labels if label.lower() in predictions
            ]

        # Other graph types remain the same
        # ...

    except Exception as e:
        return {'error': str(e)}

    return predictions

def get_impact_analysis(graph_type):
    temperature_changes = np.arange(-10, 11, 1)
    impacts = {}
    
    for label in labels:
        metric = label.lower()
        impacts[metric] = {
            'energy_efficiency': (-0.5 * temperature_changes).tolist(),
            'cooling_capacity': (0.3 * temperature_changes).tolist()
        }
    
    if graph_type in ['bar', 'column', 'line']:
        return {
            'labels': temperature_changes.tolist(),
            'datasets': [
                {'label': f'{label} - Energy Efficiency', 'data': impacts[label.lower()]['energy_efficiency']} for label in labels if label.lower() in impacts
            ] + [
                {'label': f'{label} - Cooling Capacity', 'data': impacts[label.lower()]['cooling_capacity']} for label in labels if label.lower() in impacts
            ]
        }

    elif graph_type == 'pie':
        impact_data = []
        for label in labels:
            metric = label.lower()
            impact_data.extend([
                {'label': f'{label} - Energy Efficiency', 'value': sum(impacts[metric]['energy_efficiency'])},
                {'label': f'{label} - Cooling Capacity', 'value': sum(impacts[metric]['cooling_capacity'])}
            ])
        return impact_data

    # Other graph types remain the same
    # ...

    return impacts

def graph_data_view(request):
    graph_type = request.GET.get('type', 'line')

    data = {
        'historical': get_historical_data(graph_type),
        'predictive': get_predictive_data(graph_type),
        'impact': get_impact_analysis(graph_type)
    }

    return JsonResponse(data)
