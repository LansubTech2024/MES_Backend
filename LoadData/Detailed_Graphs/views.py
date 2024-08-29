from django.http import JsonResponse
from django.db.models import Avg
from .models import TemperatureData
from datetime import timedelta
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def line_chart_popup(request):
    # Assuming we're interested in chw_in_temp for this example
    field_of_interest = 'chw_in_temp'
    
    # Get the last 30 days of data
    end_date = TemperatureData.objects.latest('device_date').device_date
    start_date = end_date - timedelta(days=30)
    
    data = TemperatureData.objects.filter(
        device_date__range=(start_date, end_date)
    ).order_by('device_date')

    # Prepare data for ARIMA model
    df = pd.DataFrame(list(data.values('device_date', field_of_interest)))
    df.set_index('device_date', inplace=True)
    
    # Fit ARIMA model
    model = ARIMA(df[field_of_interest], order=(1,1,1))
    results = model.fit()
    
    # Generate forecast for next 7 days
    forecast = results.forecast(steps=7)
    
    # Prepare predictive graph data
    predictive_data = {
        'dates': [str(date) for date in forecast.index],
        'values': forecast.values.tolist(),
    }
    
    # Calculate impact data
    current_avg = df[field_of_interest].mean()
    forecast_avg = forecast.mean()
    percent_change = ((forecast_avg - current_avg) / current_avg) * 100
    
    impact_cards = [
        {
            'title': 'Average Temperature Change',
            'value': f'{forecast_avg - current_avg:.2f}°C',
            'description': 'Predicted change in average temperature'
        },
        {
            'title': 'Percentage Change',
            'value': f'{percent_change:.2f}%',
            'description': 'Percentage change in temperature'
        },
        {
            'title': 'Efficiency Impact',
            'value': 'Medium',
            'description': 'Estimated impact on system efficiency'
        }
    ]
    
    return JsonResponse({
        'predictive_graph': predictive_data,
        'impact_cards': impact_cards
    })

def waterfall_chart_popup(request):
    # Get the last 30 days of data
    end_date = TemperatureData.objects.latest('device_date').device_date
    start_date = end_date - timedelta(days=30)
    
    data = TemperatureData.objects.filter(
        device_date__range=(start_date, end_date)
    ).order_by('device_date')

    df = pd.DataFrame(list(data.values('device_date', 'chw_in_temp', 'chw_out_temp')))
    df['temp_diff'] = df['chw_in_temp'] - df['chw_out_temp']

    # Predictive analysis
    model = ARIMA(df['temp_diff'], order=(1,1,1))
    results = model.fit()
    forecast = results.forecast(steps=7)

    predictive_data = {
        'dates': [str(date) for date in forecast.index],
        'values': forecast.values.tolist(),
    }

    # Impact analysis
    avg_diff = df['temp_diff'].mean()
    forecast_avg = forecast.mean()
    percent_change = ((forecast_avg - avg_diff) / avg_diff) * 100

    impact_cards = [
        {
            'title': 'Average Temperature Difference Change',
            'value': f'{forecast_avg - avg_diff:.2f}°C',
            'description': 'Predicted change in average temperature difference'
        },
        {
            'title': 'Percentage Change',
            'value': f'{percent_change:.2f}%',
            'description': 'Percentage change in temperature difference'
        },
        {
            'title': 'Efficiency Impact',
            'value': 'Medium' if abs(percent_change) < 10 else 'High',
            'description': 'Estimated impact on system efficiency'
        }
    ]

    return JsonResponse({
        'predictive_graph': predictive_data,
        'impact_cards': impact_cards
    })

def donut_chart_popup(request):
    # Get the last 30 days of data
    end_date = TemperatureData.objects.latest('device_date').device_date
    start_date = end_date - timedelta(days=30)
    
    data = TemperatureData.objects.filter(
        device_date__range=(start_date, end_date)
    )

    temp_ranges = {
        'Low': data.filter(chw_in_temp__lt=20).count(),
        'Medium': data.filter(chw_in_temp__gte=20, chw_in_temp__lt=25).count(),
        'High': data.filter(chw_in_temp__gte=25).count()
    }

    total = sum(temp_ranges.values())
    forecast = {k: v / total for k, v in temp_ranges.items()}

    predictive_data = {
        'labels': list(forecast.keys()),
        'values': list(forecast.values()),
    }

    impact_cards = [
        {
            'title': 'Dominant Temperature Range',
            'value': max(forecast, key=forecast.get),
            'description': 'Most frequent temperature range'
        },
        {
            'title': 'Low Temperature Percentage',
            'value': f'{forecast["Low"]*100:.2f}%',
            'description': 'Percentage of low temperature readings'
        },
        {
            'title': 'High Temperature Percentage',
            'value': f'{forecast["High"]*100:.2f}%',
            'description': 'Percentage of high temperature readings'
        }
    ]

    return JsonResponse({
        'predictive_graph': predictive_data,
        'impact_cards': impact_cards
    })

def combination_chart_popup(request):
    # Get the last 12 months of data
    end_date = TemperatureData.objects.latest('device_date').device_date
    start_date = end_date - timedelta(days=365)
    
    data = TemperatureData.objects.filter(
        device_date__range=(start_date, end_date)
    )

    df = pd.DataFrame(list(data.values('device_date', 'chw_in_temp', 'vaccum_pr')))
    df.set_index('device_date', inplace=True)
    df = df.resample('M').mean()

    # Predictive analysis
    temp_model = ARIMA(df['chw_in_temp'], order=(1,1,1))
    temp_results = temp_model.fit()
    temp_forecast = temp_results.forecast(steps=3)

    pressure_model = ARIMA(df['vaccum_pr'], order=(1,1,1))
    pressure_results = pressure_model.fit()
    pressure_forecast = pressure_results.forecast(steps=3)

    predictive_data = {
        'dates': [str(date) for date in temp_forecast.index],
        'temp_values': temp_forecast.values.tolist(),
        'pressure_values': pressure_forecast.values.tolist(),
    }

    # Impact analysis
    temp_change = (temp_forecast.mean() - df['chw_in_temp'].mean()) / df['chw_in_temp'].mean() * 100
    pressure_change = (pressure_forecast.mean() - df['vaccum_pr'].mean()) / df['vaccum_pr'].mean() * 100

    impact_cards = [
        {
            'title': 'Temperature Trend',
            'value': 'Increasing' if temp_change > 0 else 'Decreasing',
            'description': f'{abs(temp_change):.2f}% change predicted'
        },
        {
            'title': 'Pressure Trend',
            'value': 'Increasing' if pressure_change > 0 else 'Decreasing',
            'description': f'{abs(pressure_change):.2f}% change predicted'
        },
        {
            'title': 'System Status',
            'value': 'Stable' if abs(temp_change) < 5 and abs(pressure_change) < 5 else 'Fluctuating',
            'description': 'Based on temperature and pressure trends'
        }
    ]

    return JsonResponse({
        'predictive_graph': predictive_data,
        'impact_cards': impact_cards
    })