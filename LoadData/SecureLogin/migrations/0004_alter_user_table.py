# Generated by Django 5.1 on 2024-08-22 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SecureLogin', '0003_alter_user_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='SECURE_TABLE',
        ),
    ]
