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
            
            keys_to_extract = ['CHW_IN_TEMP', 'CHW_OUT_TEMP', 'COW_IN_TEMP', 'COW_OUT_TEMP', 'STEAM_COND_TEMP','HTG_TEMP','LTG_TEMP','HTHE_OUT_TEMP','SPRAY_TEMP','DL_SLN_TEMP', 'REF_TEMP','U_TUBE_TEMP', 'OVRFLW_LTG_TEMP','HTG_TOP_TEMP',
                               'HTG_BOT_TEMP','HTG_TB_ABS_DIFF_TEMP','VACCUM_PR','STRN_SLN_CONC','INT_SLN_HTG_CONC','DL_SLN_CONC','ABS_TRG_T','REF_TRG_T','MC_SP','CT_FAN_SP','CT_FAN_HYS','L_CUT_DIF_SP','L_CUT_DIF_HYS','H_CUT_DIF_SP',
                               'H_CUT_DIF_HYS','COW_IN_LOW_TRIP_SP','COW_IN_LOW_TRIP_HYS','COW_IN_HI_TRIP_SP','COW_IN_HI_TRIP_HYS','HTG_LOW_AC_DRV_SP','HTG_HI_AC_DRV_SP','HTG_TRIP_SP','HTG_TRIP_HYS','HTG_VAP_TRIP_SP','HTG_VAP_TRIP_HYS','HTG_TB_DIF_SP','HTG_TB_DIF_HYS',
                               'SCV_OP_LMT_SP','HTG_DIF_SCV_SP','HTG_DIF_SCV_HYS','ANTFRZ_SP','ANTFRZ_HYS','DT_LOG_TIME_SP','TRIPLG_TIME_SP','HTG_LVL_TMR_ABS_SP','ABLDN_SCDL_CHK_HR_SP','ABLDN_SCDL_OPR_MNS_SP','HT_DGRS_DURTN_SP','SPR_SOL_HI_HTMD_SP','SPR_SOL_HI_HTMD_HYS',
                               'SPR_SOL_CONC_LOW_SP','SPR_SOL_CONC_HI_SP','SPR_SOL_CONC_HI_HYS','REF_PMP_RN_CNTNSLY_SP', 'REF_PMP_RN_CNTNSLY_HYS','U_TUBE_SCALING_SP','COW_CRYSTALISATION_SP','MC_LOW_LMT_SP','SCV_OP_HI_LMT_SP','CHW_FLW_SP',
                               'REF_TEMP_LOW_SP','REF_TEMP_LOW_HYS','OVRFLW_HI_SP','OVRFLW_HI_HYS','CHW_FLW_LOW_SP','CHW_FLW_HI_SP','COW_FLW_LOW_SP','COW_FLW_HI_SP','STEAM_FLW_LOW_SP',
                               'STEAM_FLW_HI_SP','HTG_PR_HI_SP','HTG_PR_LOW_LMT_SP','HTG_PR_HI_LMT_SP','COW_SHUT_OFF_VLV_DLY_SP','HTG_PR_HI_HYS','MC_RDY_STS','HTG_VAP_TEMP','HTG_LVL_ABS_PMP_FREQ','SCV_PID_PROCESS_VALUE','SCV_PID_P',
                               'SCV_PID_I','DIFF_SCALING_POINT','SCV_MANUAL_OPENING','TIME']
            df = df[keys_to_extract].dropna().drop_duplicates()

            # Convert 'timestamp' column to datetime format
            if 'device_date' in df.columns:
                df['device_date'] = pd.to_datetime(df['device_date'], errors='coerce')

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