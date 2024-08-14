from django.http import JsonResponse
from django.db.models import Avg
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import numpy as np
from .models import GraphModel
from decimal import Decimal

def generate_graphs(request):
    data = GraphModel.objects.all()
    
    graphs = []
    
    # Bar chart
    plt.figure(figsize=(10, 6))
    temperatures = ['CHW In', 'CHW Out', 'COW In', 'COW Out']
    values = [
        float(data.aggregate(Avg('chw_in_temp'))['chw_in_temp__avg'] or 0),
        float(data.aggregate(Avg('chw_out_temp'))['chw_out_temp__avg'] or 0),
        float(data.aggregate(Avg('cow_in_temp'))['cow_in_temp__avg'] or 0),
        float(data.aggregate(Avg('cow_out_temp'))['cow_out_temp__avg'] or 0)
    ]
    plt.bar(temperatures, values)
    plt.title('Average Temperatures')
    plt.ylabel('Temperature')
    graphs.append({"type": "bar", "data": get_graph()})
    
    # Line plot
    plt.figure(figsize=(10, 6))
    plt.plot([float(x) for x in data.values_list('id', flat=True)],
             [float(x) for x in data.values_list('chw_in_temp', flat=True)], label='CHW In')
    plt.plot([float(x) for x in data.values_list('id', flat=True)],
             [float(x) for x in data.values_list('chw_out_temp', flat=True)], label='CHW Out')
    plt.plot([float(x) for x in data.values_list('id', flat=True)],
             [float(x) for x in data.values_list('cow_in_temp', flat=True)], label='COW In')
    plt.plot([float(x) for x in data.values_list('id', flat=True)],
             [float(x) for x in data.values_list('cow_out_temp', flat=True)], label='COW Out')
    plt.title('Temperature Trends')
    plt.xlabel('Record ID')
    plt.ylabel('Temperature')
    plt.legend()
    graphs.append({"type": "line", "data": get_graph()})
    
    # Scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter([float(x) for x in data.values_list('chw_in_temp', flat=True)],
                [float(x) for x in data.values_list('cow_out_temp', flat=True)])
    plt.title('CHW In vs COW Out Temperature')
    plt.xlabel('CHW In Temperature')
    plt.ylabel('COW Out Temperature')
    graphs.append({"type": "scatter", "data": get_graph()})
    
    # Box plot
    plt.figure(figsize=(10, 6))
    plt.boxplot([[float(x) for x in data.values_list('chw_in_temp', flat=True)],
                 [float(x) for x in data.values_list('chw_out_temp', flat=True)],
                 [float(x) for x in data.values_list('cow_in_temp', flat=True)],
                 [float(x) for x in data.values_list('cow_out_temp', flat=True)]],
                labels=['CHW In', 'CHW Out', 'COW In', 'COW Out'])
    plt.title('Temperature Distribution')
    plt.ylabel('Temperature')
    graphs.append({"type": "box", "data": get_graph()})

    # Heatmap
    plt.figure(figsize=(10, 8))
    correlation_matrix = np.corrcoef([
        [float(x) for x in data.values_list('chw_in_temp', flat=True)],
        [float(x) for x in data.values_list('chw_out_temp', flat=True)],
        [float(x) for x in data.values_list('cow_in_temp', flat=True)],
        [float(x) for x in data.values_list('cow_out_temp', flat=True)]
    ])
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', 
                xticklabels=['CHW In', 'CHW Out', 'COW In', 'COW Out'],
                yticklabels=['CHW In', 'CHW Out', 'COW In', 'COW Out'])
    plt.title('Temperature Correlation Heatmap')
    graphs.append({"type": "heatmap", "data": get_graph()})

    # Histogram
    plt.figure(figsize=(12, 6))
    plt.hist([
        [float(x) for x in data.values_list('chw_in_temp', flat=True)],
        [float(x) for x in data.values_list('chw_out_temp', flat=True)],
        [float(x) for x in data.values_list('cow_in_temp', flat=True)],
        [float(x) for x in data.values_list('cow_out_temp', flat=True)]
    ], label=['CHW In', 'CHW Out', 'COW In', 'COW Out'], bins=20)
    plt.title('Temperature Distribution Histogram')
    plt.xlabel('Temperature')
    plt.ylabel('Frequency')
    plt.legend()
    graphs.append({"type": "histogram", "data": get_graph()})
    
    # Pie Chart
    plt.figure(figsize=(10, 10))
    temp_ranges = {
        'Low': data.filter(chw_in_temp__lt=20).count(),
        'Medium': data.filter(chw_in_temp__gte=20, chw_in_temp__lt=30).count(),
        'High': data.filter(chw_in_temp__gte=30).count()
    }
    plt.pie(temp_ranges.values(), labels=temp_ranges.keys(), autopct='%1.1f%%')
    plt.title('CHW In Temperature Range Distribution')
    graphs.append({"type": "pie", "data": get_graph()})
    
    return JsonResponse({"graphs": graphs})

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode('utf-8')
    buffer.close()
    return graph
