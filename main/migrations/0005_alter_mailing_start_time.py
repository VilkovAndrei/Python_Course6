# Generated by Django 5.0.6 on 2024-05-19 18:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_mailing_create_time_mailing_start_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 19, 21, 2, 58, 960843), verbose_name='Дата и время старта рассылки'),
        ),
    ]
