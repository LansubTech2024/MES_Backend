from django.db import models

class Machine(models.Model):
    chw_in_temp = models.FloatField()
    chw_out_temp = models.FloatField()
    cow_in_temp = models.FloatField()
    cow_out_temp = models.FloatField()

    class Meta:
        db_table = 'MACHINES_TABLE'

