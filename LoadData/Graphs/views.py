import oracledb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def fetch_all_charts(request):
    # Connect to the Oracle database using oracledb
    connection = oracledb.connect(
        user='SYS',
        password='Lansub',
        dsn='localhost:1521/orcl',
        mode=oracledb.SYSDBA
    )
    
    # Execute the query and fetch data into a DataFrame
    query = 'SELECT * FROM MACHINES_TABLE'  # Update with your query
    df = pd.read_sql(query, con=connection)
    
    # Dictionary to store chart images
    charts = {}
    
    # Bar Chart
    buf = BytesIO()
    plt.figure()
    df.plot(kind='bar', x='CHW_IN_TEMP', y='CHW_OUT_TEMP')  # Adjust columns as needed
    plt.title('Bar Chart Example')
    plt.savefig(buf, format='png')
    buf.seek(0)
    charts['bar'] = buf.getvalue().decode('latin1')
    plt.close()

    # Pie Chart
    buf = BytesIO()
    plt.figure()
    df.groupby('category_column')['COW_OUT_TEMP'].sum().plot(kind='pie', autopct='%1.1f%%')  # Adjust columns as needed
    plt.title('Pie Chart Example')
    plt.savefig(buf, format='png')
    buf.seek(0)
    charts['pie'] = buf.getvalue().decode('latin1')
    plt.close()

    # Heatmap
    buf = BytesIO()
    plt.figure()
    heatmap_data = df.pivot('CHW_OUT_TEMP', 'CHW_IN_TEMP', 'COW_OUT_TEMP')  # Adjust columns as needed
    sns.heatmap(heatmap_data, annot=True, cmap='coolwarm')
    plt.title('Heatmap Example')
    plt.savefig(buf, format='png')
    buf.seek(0)
    charts['heatmap'] = buf.getvalue().decode('latin1')
    plt.close()

    # Histogram
    buf = BytesIO()
    plt.figure()
    df['COW_OUT_TEMP'].plot(kind='hist', bins=10)  # Adjust columns and bins as needed
    plt.title('Histogram Example')
    plt.savefig(buf, format='png')
    buf.seek(0)
    charts['histogram'] = buf.getvalue().decode('latin1')
    plt.close()

    # Scatter Plot
    buf = BytesIO()
    plt.figure()
    df.plot(kind='scatter', x='CHW_IN_TEMP', y='CHW_OUT_TEMP')  # Adjust columns as needed
    plt.title('Scatter Plot Example')
    plt.savefig(buf, format='png')
    buf.seek(0)
    charts['scatter'] = buf.getvalue().decode('latin1')
    plt.close()

    # Box Plot
    buf = BytesIO()
    plt.figure()
    df[['COW_OUT_TEMP']].plot(kind='box')  # Adjust columns as needed
    plt.title('Box Plot Example')
    plt.savefig(buf, format='png')
    buf.seek(0)
    charts['box'] = buf.getvalue().decode('latin1')
    plt.close()

    # Return all charts as JSON
    return JsonResponse(charts)