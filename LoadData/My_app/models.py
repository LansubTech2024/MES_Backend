from django.db import models

class Device(models.Model):
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
        db_table = 'MANUFACTURING_TABLE'

