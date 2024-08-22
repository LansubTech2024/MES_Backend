from rest_framework import serializers
from .models import Product

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['chw_in_temp', 'chw_out_temp', 'cow_in_temp', 'cow_out_temp']
