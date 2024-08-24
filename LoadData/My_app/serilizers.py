from rest_framework import serializers
from .models import Device

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            'chw_in_temp', 'chw_out_temp', 'cow_in_temp', 'cow_out_temp',
            'steam_cond_temp', 'htg_temp', 'ltg_temp', 'hthe_out_temp', 'sray_temp',
            'dl_sln_temp', 'ref_temp', 'u_tube_temp', 'ovrflw_lgt_temp', 'htg_top_temp',
            'htg_bot_temp', 'htg_tb_abs_diff_temp', 'vaccum_pr', 'ref_temp_low_sp', 
            'ref_temp_low_hys', 'htg_hr_hi_sp', 'htg_pr_low_lmt_sp', 'htg_pr_hi_lmt_sp', 
            'htg_pr_hi_hys', 'htg_vap_temp', 'device_date'
        ]
