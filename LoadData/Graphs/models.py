from django.db import models

class GraphModel(models.Model):
    chw_in_temp = models.FloatField()
    chw_out_temp = models.FloatField()
    cow_in_temp = models.FloatField()
    cow_out_temp = models.FloatField()
    steam_cond_temp = models.FloatField()
    htg_temp = models.FloatField()
    ltg_temp = models.FloatField()
    hthe_out_temp = models.FloatField()
    spray_temp = models.FloatField()
    dl_sln_temp = models.FloatField()
    ref_temp = models.FloatField()
    u_tube_temp = models.FloatField()
    ovrflw_ltg_temp = models.FloatField()
    htg_top_temp = models.FloatField()
    htg_bot_temp = models.FloatField()
    htg_tb_abs_diff_temp = models.FloatField()
    vaccum_pr = models.FloatField()
    ref_temp_low_sp = models.FloatField()
    ref_temp_low_hys = models.FloatField()
    htg_pr_hi_sp = models.FloatField()
    htg_pr_low_lmt_sp = models.FloatField()
    htg_pr_hi_lmt_sp = models.FloatField()
    htg_pr_hi_hys = models.FloatField()
    htg_vap_temp = models.FloatField()
    device_date = models.DateTimeField()
    
    class Meta:
        managed = False  # If you don't want Django to manage this table
        db_table = 'MANUFACTURING_TABLE'  # Replace with your actual table name
    
    def __str__(self):
        return (
            f"Date: {self.device_date}, "
            f"CHW In: {self.chw_in_temp}, CHW Out: {self.chw_out_temp}, "
            f"COW In: {self.cow_in_temp}, COW Out: {self.cow_out_temp}, "
            f"Steam Cond: {self.steam_cond_temp}, HTG Temp: {self.htg_temp}, "
            f"LTG Temp: {self.ltg_temp}, HTHE Out: {self.hthe_out_temp}, "
            f"Sray Temp: {self.spray_temp}, DL SLN Temp: {self.dl_sln_temp}, "
            f"Ref Temp: {self.ref_temp}, U Tube Temp: {self.u_tube_temp}, "
            f"Ovrflw Lgt Temp: {self.ovrflw_ltg_temp}, HTG Top Temp: {self.htg_top_temp}, "
            f"HTG Bot Temp: {self.htg_bot_temp}, HTG TB Abs Diff Temp: {self.htg_tb_abs_diff_temp}, "
            f"Vacuum PR: {self.vaccum_pr}, Ref Temp Low SP: {self.ref_temp_low_sp}, "
            f"Ref Temp Low HYS: {self.ref_temp_low_hys}, HTG HR Hi SP: {self.htg_pr_hi_sp}, "
            f"HTG PR Low Lmt SP: {self.htg_pr_low_lmt_sp}, HTG PR Hi Lmt SP: {self.htg_pr_hi_lmt_sp}, "
            f"HTG PR Hi HYS: {self.htg_pr_hi_hys}, HTG Vap Temp: {self.htg_vap_temp}"
        )
