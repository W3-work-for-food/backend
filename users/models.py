from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    username = models.CharField(max_length=150)
    email = models.EmailField(
        max_length=254, unique=True,
        verbose_name='E-mail')
    first_name = models.CharField(
        max_length=64,
        verbose_name='Имя'
    )
    middle_name = models.CharField(
        max_length=64,
        verbose_name='Отчество'
    )
    last_name = models.CharField(
        max_length=64,
        verbose_name='Фамилия'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username
