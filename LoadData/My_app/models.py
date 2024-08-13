from django.db import models

class Machine(models.Model):
    id = models.AutoField(primary_key=True)
    chw_in_temp = models.FloatField()
    chw_out_temp = models.FloatField()
    cow_in_temp = models.FloatField()
    cow_out_temp = models.FloatField()
    time = models.TimeField()

    class Meta:
        db_table = 'SCHEMA_NAME.MACHINES_TABLE'

