import json
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Machine
from .serilizers import MachineSerializer
from datetime import datetime

class ImportMachinesView(APIView):
    def post(self, request, *args, **kwargs):
        
        try:
             # Specify the path to your JSON file
            json_file_path = r'C:\Users\Lenovo\Desktop\MES_Frontend\Django_backend\LoadData\data.json'  # Update this to your actual file path

            # Load JSON data from the file
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)

            # Check if data is a list
            if isinstance(data, list):
                # Convert JSON list to DataFrame
                df = pd.json_normalize(data)
            else:
                return Response({"error": "Expected a list of objects in JSON file."}, status=status.HTTP_400_BAD_REQUEST)
            keys_to_extract = ['CHW_IN_TEMP', 'CHW_OUT_TEMP', 'COW_IN_TEMP', 'COW_OUT_TEMP']
            df = df[keys_to_extract].dropna().drop_duplicates()

            # Clear existing records
            Machine.objects.all().delete()

            # Insert new data
            machines = [
                Machine(
                    chw_in_temp=row['CHW_IN_TEMP'],
                    chw_out_temp=row['CHW_OUT_TEMP'],
                    cow_in_temp=row['COW_IN_TEMP'],
                    cow_out_temp=row['COW_OUT_TEMP'],
                    time=datetime.strptime(row['TIME'], '%d/%m/%Y %H:%M:%S').time()
                )
                for _, row in df.iterrows()
            ]
            Machine.objects.bulk_create(machines)

            return Response({"success": "Data successfully inserted into Oracle SQL!"}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
