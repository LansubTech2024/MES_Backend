from django.http import JsonResponse
from django.db.models import Avg
from .models import TemperatureData
from datetime import timedelta , datetime
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

def line_chart_popup(request):
    # Time Series Forecasting Chart for Line Chart
    field_of_interest = 'chw_in_temp'
    
    end_date = TemperatureData.objects.latest('device_date').device_date
    start_date = end_date - timedelta(days=30)
    
    data = TemperatureData.objects.filter(
        device_date__range=(start_date, end_date)
    ).order_by('device_date')

    df = pd.DataFrame(list(data.values('device_date', field_of_interest)))
    df.set_index('device_date', inplace=True)
    
    model = ARIMA(df[field_of_interest], order=(1,1,1))
    results = model.fit()
    
    forecast = results.forecast(steps=7)
    last_date = df.index[-1]
    future_dates = [last_date + timedelta(days=i+1) for i in range(len(forecast))]
    
    predictive_data = {
        'type': 'time_series_forecast',
        'dates': [date.strftime('%Y-%m-%d') for date in future_dates],
        'values': forecast.values.tolist(),
    }
    
    current_avg = df[field_of_interest].mean()
    forecast_avg = forecast.mean()
    percent_change = ((forecast_avg - current_avg) / current_avg) * 100

    # Function to determine efficiency impact
    def get_efficiency_impact(percent_change):
        abs_change = abs(percent_change)
        if abs_change < 2:
            return 'Low'
        elif abs_change < 5:
            return 'Medium'
        else:
            return 'High'
    
    efficiency_impact = get_efficiency_impact(percent_change)

     # Generate recommendation based on efficiency impact
    if efficiency_impact == 'Low':
        recommendation = "The machine's efficiency is good. Continue maintaining current operational parameters."
    elif efficiency_impact == 'Medium':
        recommendation = "Consider adjusting the cooling system or reviewing recent maintenance logs to improve efficiency."
    else:
        recommendation = "Immediate attention required. Check for system anomalies and consider reducing load to bring the machine back to normal operating conditions."
    
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
            'value': efficiency_impact,
            'description': 'Estimated impact on system efficiency'
        }
    ]
    
    return JsonResponse({
        'predictive_graph': predictive_data,
        'impact_cards': impact_cards,
        'recommendation' : recommendation,
    })

def waterfall_chart_popup(request):
   # Line Chart for Temperature Data
    end_date = TemperatureData.objects.latest('device_date').device_date
    start_date = end_date - timedelta(days=30)
    
    data = TemperatureData.objects.filter(
        device_date__range=(start_date, end_date)
    ).order_by('device_date')
    
    df = pd.DataFrame(list(data.values('device_date', 'chw_in_temp', 'chw_out_temp')))
    df['temp_diff'] = df['chw_in_temp'] - df['chw_out_temp']
    
    predictive_data = {
        'type': 'line_chart',
        'dates': [date.strftime('%Y-%m-%d') for date in df['device_date']],
        'chw_in_temp': df['chw_in_temp'].tolist(),
        'chw_out_temp': df['chw_out_temp'].tolist(),
        'temp_diff': df['temp_diff'].tolist(),
    }
    
    avg_diff = df['temp_diff'].mean()
    max_diff = df['temp_diff'].max()
    min_diff = df['temp_diff'].min()

    # Calculate the trend of temperature difference
    temp_diff_trend = df['temp_diff'].iloc[-1] - df['temp_diff'].iloc[0]
    
    impact_cards = [
        {
            'title': 'Average Temperature Difference',
            'value': f'{avg_diff:.2f}°C',
            'description': 'Average daily temperature difference'
        },
        {
            'title': 'Maximum Temperature Difference',
            'value': f'{max_diff:.2f}°C',
            'description': 'Highest recorded temperature difference'
        },
        {
            'title': 'Minimum Temperature Difference',
            'value': f'{min_diff:.2f}°C',
            'description': 'Lowest recorded temperature difference'
        },
        {
            'title': 'Temperature Difference Trend',
            'value': 'Increasing' if temp_diff_trend > 0 else 'Decreasing',
            'description': f'{abs(temp_diff_trend):.2f}°C change over period'
        }
    ]

    # Generate recommendation based on temperature difference trends
    if abs(temp_diff_trend) < 1:
        recommendation = "The temperature difference between input and output is stable. Continue current operational practices."
    elif temp_diff_trend > 1:
        recommendation = "The temperature difference is increasing. This could indicate improving efficiency, but check if it's within optimal range for your system."
    else:
        recommendation = "The temperature difference is decreasing. This might indicate reduced cooling efficiency. Consider inspecting the system for potential issues."
    
    
    return JsonResponse({
        'predictive_graph': predictive_data,
        'impact_cards': impact_cards,
        'recommendation' : recommendation
    })

def donut_chart_popup(request):
    # Line Chart for Temperature Data
    end_date = TemperatureData.objects.latest('device_date').device_date
    start_date = end_date - timedelta(days=30)
    
    data = TemperatureData.objects.filter(
        device_date__range=(start_date, end_date)
    ).order_by('device_date')
    
    dates = [entry.device_date.strftime('%Y-%m-%d') for entry in data]
    temperatures = [entry.chw_in_temp for entry in data]
    
    predictive_data = {
        'type': 'line',
        'labels': dates,
        'datasets': [{
            'label': 'Temperature',
            'data': temperatures,
        }]
    }
    
    # Calculate temperature ranges
    temp_ranges = {
        'Low': sum(1 for temp in temperatures if temp < 20),
        'Medium': sum(1 for temp in temperatures if 20 <= temp < 25),
        'High': sum(1 for temp in temperatures if temp >= 25)
    }
    
    total = sum(temp_ranges.values())
    forecast = {k: v / total for k, v in temp_ranges.items()}
    
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
    
    # Generate recommendation based on the dominant temperature range
    dominant_range = max(forecast, key=forecast.get)
    if dominant_range == 'Low':
        recommendation = "The majority of readings fall in the low temperature range. Consider evaluating if the cooling system is over-performing."
    elif dominant_range == 'High':
        recommendation = "High temperature readings dominate. This could indicate potential inefficiency in the cooling system. Investigate for any issues."
    else:
        recommendation = "Temperature readings are within an optimal range. Continue monitoring for consistent performance."
    
    return JsonResponse({
        'predictive_graph': predictive_data,
        'impact_cards': impact_cards,
        'recommendation': recommendation
    })
def combination_chart_popup(request):
    # Overlay Combination Chart for Combination Chart
    end_date = TemperatureData.objects.latest('device_date').device_date
    start_date = end_date - timedelta(days=365)
    
    data = TemperatureData.objects.filter(
        device_date__range=(start_date, end_date)
    )

    df = pd.DataFrame(list(data.values('device_date', 'chw_in_temp', 'vaccum_pr')))
    df.set_index('device_date', inplace=True)
    df = df.resample('M').mean()

    temp_model = ARIMA(df['chw_in_temp'], order=(1,1,1))
    temp_results = temp_model.fit()
    temp_forecast = temp_results.forecast(steps=3)

    pressure_model = ARIMA(df['vaccum_pr'], order=(1,1,1))
    pressure_results = pressure_model.fit()
    pressure_forecast = pressure_results.forecast(steps=3)

    predictive_data = {
        'type': 'overlay_combination',
        'dates': [str(date) for date in temp_forecast.index],
        'temp_values': temp_forecast.values.tolist(),
        'pressure_values': pressure_forecast.values.tolist(),
    }

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

    # Generate recommendation based on temperature and pressure trends
    if abs(temp_change) < 5 and abs(pressure_change) < 5:
        recommendation = "The system is stable. No immediate action is needed, but continue regular monitoring."
    elif temp_change > 5 or pressure_change > 5:
        recommendation = "Significant changes in temperature or pressure detected. Consider inspecting the system for potential issues."
    else:
        recommendation = "Moderate fluctuations observed. Keep an eye on the trends to prevent any future system instability."

    return JsonResponse({
        'predictive_graph': predictive_data,
        'impact_cards': impact_cards,
        'recommendation': recommendation
    })