# Generated by Django 5.1 on 2024-08-22 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SecureLogin', '0004_alter_user_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='Email'),
        ),
    ]
