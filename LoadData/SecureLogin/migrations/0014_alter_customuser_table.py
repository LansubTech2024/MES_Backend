# Generated by Django 5.1 on 2024-08-28 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SecureLogin', '0013_customuser_date_joined_alter_customuser_last_login'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='customuser',
            table='CUSTOMUSER_LOGIN',
        ),
    ]
