# Generated by Django 5.1 on 2024-08-22 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SecureLogin', '0006_alter_user_last_login_alter_user_password_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='AUTH_TABLE',
        ),
    ]
