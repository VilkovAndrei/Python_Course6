from datetime import datetime

from django.conf import settings

from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """Модель клиента сервиса рассылок"""
    email = models.EmailField(max_length=150, unique=True, verbose_name='Почта')
    name = models.CharField(max_length=100, verbose_name='ФИО или Наименование')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Пользователь', null=True)

    def __str__(self):
        return f'{self.name} {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('id',)


class MessageMailing(models.Model):
    """Модель сообщения рассылки"""
    subject = models.CharField(max_length=150, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Текс сообщения', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Пользователь', null=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение рассылки'
        verbose_name_plural = 'Сообщения рассылки'
        ordering = ('id',)


class Mailing(models.Model):
    """Модель рассылки"""

    class FrequencyMailing(models.TextChoices):
        """Периодичность рассылки"""
        ONE_TIME = "Разовая", "Разовая"
        ONE_DAY = "Раз в день", "Раз в день"
        ONE_WEEK = "Раз в неделю", "Раз в неделю"
        ONE_MONTH = "Раз в месяц", "Раз в месяц"

    class StatusMailing(models.TextChoices):
        """Статус рассылки"""
        CREATED = "Создана", "Создана"
        STARTED = "Запущена", "Запущена"
        COMPLETED = "Завершена", "Завершена"

    start_time = models.DateTimeField(default=datetime.now(), verbose_name='Дата и время старта рассылки')
    stop_time = models.DateTimeField(default=None, verbose_name='Дата и время окончания рассылки', **NULLABLE)
    frequency_mailing = models.CharField(max_length=50, default=FrequencyMailing.ONE_DAY,
                                         choices=FrequencyMailing, verbose_name='Периодичность рассылки')
    status_mailing = models.CharField(max_length=50, default=StatusMailing.CREATED,
                                      choices=StatusMailing, verbose_name='Статус рассылки')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты рассылки')
    message = models.ForeignKey(MessageMailing, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Пользователь', null=True)
    is_active = models.BooleanField(default=True, verbose_name='признак блокировки')

    def __str__(self):
        return f'{self.start_time} {self.frequency_mailing} {self.status_mailing}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('id',)

        permissions = [
            (
                "set_is_active_status",
                "Can set 'is_active' status"
            )
        ]


class AttemptMailing(models.Model):
    """Модель попытки рассылки"""
    time_last_mailing = models.DateTimeField(verbose_name='Дата и время последней попытки рассылки', auto_now_add=True)
    status = models.BooleanField(verbose_name='Статус попытки рассылки')
    server_response = models.CharField(verbose_name='Ответ сервера', **NULLABLE)
    mailing = models.ForeignKey(Mailing, verbose_name='Рассылки', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.mailing} {self.time_last_mailing} {self.status}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
        ordering = ('id',)
