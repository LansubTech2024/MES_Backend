# Generated by Django 5.1 on 2024-08-27 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SecureLogin', '0007_alter_user_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='AUTH_LOGIN_TABLE',
        ),
    ]
