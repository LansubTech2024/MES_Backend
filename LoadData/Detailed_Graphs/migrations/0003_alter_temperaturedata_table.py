# Generated by Django 5.1 on 2024-08-21 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Detailed_Graphs', '0002_alter_temperaturedata_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='temperaturedata',
            table='MACHINE_TABLE',
        ),
    ]
