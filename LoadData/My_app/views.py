import json
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Device
from .serilizers import MachineSerializer
from datetime import datetime
import time

class ImportMachinesView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Specify the path to your JSON file
            json_file_path = r'C:\Users\Lenovo\Desktop\MES_Backend\LoadData\data.json' 

            # Load JSON data from the file
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)

            # Check if data is a list
            if isinstance(data, list):
                # Convert JSON list to DataFrame
                df = pd.json_normalize(data)
            else:
                return Response({"error": "Expected a list of objects in JSON file."}, status=status.HTTP_400_BAD_REQUEST)
            

            keys_to_extract = ['CHW_IN_TEMP', 'CHW_OUT_TEMP', 'COW_IN_TEMP', 'COW_OUT_TEMP', 'STEAM_COND_TEMP','HTG_TEMP','LTG_TEMP','HTHE_OUT_TEMP','SPRAY_TEMP','DL_SLN_TEMP', 'REF_TEMP','U_TUBE_TEMP', 'OVRFLW_LTG_TEMP','HTG_TOP_TEMP',
                               'HTG_BOT_TEMP','HTG_TB_ABS_DIFF_TEMP','VACCUM_PR','REF_TEMP_LOW_SP','REF_TEMP_LOW_HYS','HTG_PR_HI_SP','HTG_PR_LOW_LMT_SP','HTG_PR_HI_LMT_SP','HTG_PR_HI_HYS','HTG_VAP_TEMP','TIME']
            df = df[keys_to_extract].dropna().drop_duplicates()


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
                machine, created = Device.objects.get_or_create(
                    chw_in_temp=row['CHW_IN_TEMP'],
                    chw_out_temp=row['CHW_OUT_TEMP'],
                    cow_in_temp=row['COW_IN_TEMP'],
                    cow_out_temp=row['COW_OUT_TEMP'],
                    steam_cond_temp=row['STEAM_COND_TEMP'],
                    htg_temp=row['HTG_TEMP'],
                    ltg_temp=row['LTG_TEMP'],
                    hthe_out_temp=row['HTHE_OUT_TEMP'],
                    spray_temp=row['SPRAY_TEMP'],
                    dl_sln_temp=row['DL_SLN_TEMP'],
                    ref_temp=row['REF_TEMP'],
                    u_tube_temp=row['U_TUBE_TEMP'],
                    ovrflw_ltg_temp=row['OVRFLW_LTG_TEMP'],
                    htg_top_temp=row['HTG_TOP_TEMP'],
                    htg_bot_temp=row['HTG_BOT_TEMP'],
                    htg_tb_abs_diff_temp=row['HTG_TB_ABS_DIFF_TEMP'],
                    vaccum_pr=row['VACCUM_PR'],
                    ref_temp_low_sp=row['REF_TEMP_LOW_SP'],
                    ref_temp_low_hys=row['REF_TEMP_LOW_HYS'],
                    htg_pr_hi_sp=row['HTG_PR_HI_SP'],
                    htg_pr_low_lmt_sp=row['HTG_PR_LOW_LMT_SP'],
                    htg_pr_hi_lmt_sp=row['HTG_PR_HI_LMT_SP'],
                    htg_pr_hi_hys=row['HTG_PR_HI_HYS'],
                    htg_vap_temp=row['HTG_VAP_TEMP'],
                    device_date=row['TIME'],
                )
                if created:
                    new_machines.append(machine)

                # Add a delay of 3 seconds before processing the next record
                    time.sleep(3)

            return Response({
                "success": f"{len(new_machines)} new records successfully inserted into Oracle SQL!",
                "total_records": Device.objects.count()
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)