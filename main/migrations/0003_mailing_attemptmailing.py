# Generated by Django 5.0.6 on 2024-05-19 07:29

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_messagemailing'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=datetime.datetime(2024, 5, 19, 10, 29, 20, 645531), verbose_name='Дата и время создания рассылки')),
                ('frequency_mailing', models.CharField(choices=[('Разовая', 'Разовая'), ('Раз в день', 'Раз в день'), ('Раз в неделю', 'Раз в неделю'), ('Раз в месяц', 'Раз в месяц')], default='Раз в день', max_length=50, verbose_name='Периодичность рассылки')),
                ('status_mailing', models.CharField(choices=[('Создана', 'Создана'), ('Запущена', 'Запущена'), ('Завершена', 'Завершена')], default='Создана', max_length=50, verbose_name='Статус рассылки')),
                ('clients', models.ManyToManyField(to='main.client', verbose_name='Клиенты рассылки')),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.messagemailing', verbose_name='Сообщение')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользватель')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='AttemptMailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_last_mailing', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки рассылки')),
                ('status', models.BooleanField(verbose_name='Статус попытки рассылки')),
                ('server_response', models.CharField(blank=True, null=True, verbose_name='Ответ сервера')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.mailing', verbose_name='Рассылки')),
            ],
            options={
                'verbose_name': 'Попытка рассылки',
                'verbose_name_plural': 'Попытки рассылки',
                'ordering': ('id',),
            },
        ),
    ]
