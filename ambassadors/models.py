from django.db import models
from users.models import User
from django.contrib.auth import get_user_model

Ambassador = get_user_model()



class Merch(models.Model):
    """Модель для мерча"""
    merch_type = models.CharField(
        verbose_name='Наименование мерча',
        max_length=50,
    )
    category = models.CharField(
        verbose_name='Категория мерча',
        max_length=50,
    )
    price = models.SmallIntegerField(
        verbose_name='Стоимость мерча',
    )

    class Meta:
        verbose_name = 'Мерч'
        verbose_name_plural = 'Мерч'


    def __str__(self):
        return f'{self.merch_type}'
    

class MerchSent(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Менеджер',
    )
    ambassador = models.ForeignKey(
        Ambassador,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ambassador = models.ForeignKey(
        Ambassador,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        abstract = True
