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
            json_file_path = r'C:\Users\Lenovo\Desktop\MES_Backend\LoadData\data.json'  # Update this to your actual file path

            # Load JSON data from the file
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)

            # Check if data is a list
            if isinstance(data, list):
                # Convert JSON list to DataFrame
                df = pd.json_normalize(data)
            else:
                return Response({"error": "Expected a list of objects in JSON file."}, status=status.HTTP_400_BAD_REQUEST)
            
            keys_to_extract = ['CHW_IN_TEMP', 'CHW_OUT_TEMP', 'COW_IN_TEMP', 'COW_OUT_TEMP', 'TIME']
            df = df[keys_to_extract].dropna()

            # Convert 'timestamp' column to datetime format
            if 'device_date' in df.columns:
                df['device_date'] = pd.to_datetime(df['device_date'], errors='coerce')

            # Remove rows with invalid dates
            df = df.dropna(subset=['TIME'])
            
            # Remove duplicate rows
            df = df.drop_duplicates()

            # Insert new data without deleting existing records
            new_machines = []
            for _, row in df.iterrows():
                machine, created = Machine.objects.get_or_create(
                    chw_in_temp=row['CHW_IN_TEMP'],
                    chw_out_temp=row['CHW_OUT_TEMP'],
                    cow_in_temp=row['COW_IN_TEMP'],
                    cow_out_temp=row['COW_OUT_TEMP'],
                    device_date=row['TIME'],
                )
                if created:
                    new_machines.append(machine)

            return Response({
                "success": f"{len(new_machines)} new records successfully inserted into Oracle SQL!",
                "total_records": Machine.objects.count()
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)