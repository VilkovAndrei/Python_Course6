from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models

from config.settings import EMAIL_HOST_USER

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    comment = models.CharField(max_length=256, verbose_name='комментарий', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def send_confirm_email(self, subject, message):
        send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [f'{self.email}'],
            fail_silently=False,
        )
