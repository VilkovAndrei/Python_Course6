from datetime import datetime

from django.conf import settings

from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(max_length=150, unique=True, verbose_name='Почта')
    name = models.CharField(max_length=100, verbose_name='ФИО или Наименование')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Пользователь', null=True)

    def __repr__(self):
        return f'{self.name} {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('id',)
