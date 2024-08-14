from django.db import models

class GraphModel(models.Model):
    chw_in_temp = models.FloatField()
    chw_out_temp = models.FloatField()
    cow_in_temp = models.FloatField()
    cow_out_temp = models.FloatField()
    
    # Add any other fields if necessary
    
    class Meta:
        managed = False  # If you don't want Django to manage this table
        db_table = 'MACHINES_TABLE'  # Replace with your actual table name
    
    def __str__(self):
        return f"CHW In: {self.chw_in_temp}, CHW Out: {self.chw_out_temp}, COW In: {self.cow_in_temp}, COW Out: {self.cow_out_temp}"
