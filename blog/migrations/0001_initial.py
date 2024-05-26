# Generated by Django 5.0.6 on 2024-05-24 19:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.CharField(max_length=255, unique=True, verbose_name='Слаг')),
                ('description', models.TextField(verbose_name='Содержание')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='posts', verbose_name='Изображение')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('count_view', models.SmallIntegerField(default=0, verbose_name='Количество просмотров')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'статья',
                'verbose_name_plural': 'статьи',
                'permissions': [('set_published_status', 'Can set published status')],
            },
        ),
    ]
