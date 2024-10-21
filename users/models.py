from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

NULLABLE = dict(null=True, blank=True)


class User(AbstractUser):
    """Класс-пользователя"""
    email = models.EmailField(unique=True, verbose_name='Электронная почта', help_text='Введите электронную почту')
    phone = models.CharField(max_length=100, verbose_name='Телефон', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    chat_id = models.BigIntegerField(verbose_name='CHAT ID от телеграмма', **NULLABLE)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', ]

    def __repr__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('pk',)
