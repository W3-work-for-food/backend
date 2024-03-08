from django.db import models
from django.utils.translation import gettext_lazy as _
from ambassadors.validators import (
    validate_promo_code, validate_tg_name, UNIQUE_TG_NAME_ERROR
)
from users.models import User

STATUS_CHOICES = (
    ('active', 'Активный'),
    ('paused', 'На паузе'),
    ('non_ambassador', 'Не амбассадор'),
    ('clarifying', 'Уточняется'),
)

GENDER_CHOICES = (('male', 'М'), ('female', 'Ж'))

CLOTHING_SIZE_CHOICES = (
    ('extra_small', 'XS'),
    ('small', 'S'),
    ('medium', 'M'),
    ('large', 'L'),
    ('extra_large', 'XL'),
)
NOTIFICATION_TYPE_CHOICES = (
    ('new_profile', 'Новая анкета'),
    ('new_content', 'Новый контент'),
    ('guide_completed', 'Гайд выполнен'),
)
NOTIFICATION_STATUS_CHOICES = (
    ('read', 'Прочитано'),
    ('unread', 'Непрочитано'),
)


class Merch(models.Model):
    """Модель мерча."""
    merch_type = models.CharField(
        max_length=50,
        verbose_name='Наименование мерча',
    )
    category = models.CharField(max_length=50, verbose_name='Категория мерча')

    price = models.PositiveIntegerField(verbose_name='Стоимость мерча')

    class Meta:
        verbose_name = 'Мерч'
        verbose_name_plural = 'Мерч'

    def __str__(self):
        return f'{self.merch_type}'


class Profile(models.Model):
    """Модель амбассадора."""
    email = models.EmailField(max_length=255, verbose_name='Email')
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, verbose_name='Пол'
    )
    job = models.CharField(max_length=255, verbose_name='Работа')
    clothing_size = models.CharField(
        max_length=11,
        choices=CLOTHING_SIZE_CHOICES,
        verbose_name='Размер одежды'
    )
    foot_size = models.IntegerField(verbose_name='Размер обуви')
    blog_link = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Ссылка на блог'
    )
    additional = models.TextField(
        max_length=1024,
        blank=True,
        null=True,
        verbose_name='Дополнительная информация'
    )
    education = models.TextField(verbose_name='Образование')
    education_path = models.TextField(verbose_name='Путь обучения')
    education_goal = models.TextField(verbose_name='Цель обучения')
    phone = models.CharField(max_length=255, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Профиль амбассадора'
        verbose_name_plural = 'Профили амбассадоров'


class Content(models.Model):
    """Модель контента."""
    link = models.URLField(
        max_length=255,
        unique=False,
        blank=False,
        verbose_name='Ссылка на контент'
    )
    date = models.DateTimeField(
        max_length=30,
        auto_now_add=True,
        unique=False,
        blank=False,
        verbose_name='Дата добавления контента'
    )
    guide_condition = models.BooleanField(
        unique=False,
        blank=False,
        verbose_name='Статус гайда'
    )

    class Meta:
        verbose_name = 'Контент'
        verbose_name_plural = 'Контент'


class Address(models.Model):
    """Модель адреса амбассадора."""
    country = models.CharField(max_length=255, verbose_name='Страна')
    region = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Район, область'
    )
    city = models.CharField(max_length=255, verbose_name='Город')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    postal_code = models.PositiveSmallIntegerField(
        verbose_name='Почтовый индекс'
    )

    class Meta:
        verbose_name = 'Адрес амбассадора'
        verbose_name_plural = 'Адреса амбассадоров'


class Ambassador(models.Model):
    """Модель амбассадора."""
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления амбассадора'
    )
    telegram = models.CharField(
        max_length=35,
        validators=[validate_tg_name],
        unique=True,
        verbose_name='Телеграм',
        error_messages={
            'unique': _(f"{UNIQUE_TG_NAME_ERROR}"),
        }
    )
    name = models.CharField(max_length=255, verbose_name='ФИО')
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='ambassador',
        verbose_name='Профиль'
    )
    status = models.CharField(
        max_length=35,
        choices=STATUS_CHOICES,
        verbose_name='Статус'
    )
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        related_name='ambassador',
        verbose_name='Адрес амбассадора'
    )
    content = models.OneToOneField(
        Content,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Контент'
    )
    comment = models.TextField(
        max_length=1024,
        blank=True,
        verbose_name='Комментарий'
    )
    guide_status = models.BooleanField(
        default=False,
        verbose_name='Статус гайда'
    )

    class Meta:
        verbose_name = 'Амбассадор'
        verbose_name_plural = 'Амбассадоры'


class Notification(models.Model):
    """Модель уведомлений."""
    pub_date = models.DateTimeField(auto_now_add=True)
    ambassador = models.ForeignKey(
        Ambassador,
        on_delete=models.CASCADE,
        verbose_name='Амбассадор',
    )
    type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPE_CHOICES,
        default='Новая анкета'
    )
    status = models.CharField(
        max_length=20,
        choices=NOTIFICATION_STATUS_CHOICES,
        default='Непрочитано'
    )

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'


class Promocode(models.Model):
    """Модель промокодов."""
    ambassador = models.ForeignKey(
        Ambassador,
        on_delete=models.CASCADE,
        related_name='promocodes',
        verbose_name='Промокод'
    )
    promocode = models.CharField(
        max_length=255,
        validators=[validate_promo_code],
        verbose_name='Промокод'
    )
    is_active = models.BooleanField(verbose_name='Статус')

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'


class SentMerch(models.Model):
    """Модель мерч в отправке."""
    date = models.DateTimeField(
        max_length=30,
        auto_now_add=True,
        unique=False,
        blank=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name='Менеджер',
    )
    ambassador = models.ForeignKey(
        Ambassador,
        on_delete=models.CASCADE,
        verbose_name='Амбассадор',
    )
    merch = models.ManyToManyField(
        Merch,
        verbose_name='Мерч',
        blank=False,
        related_name='merch'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Стоимость',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Мерч в отправке'
        verbose_name_plural = 'Мерч в отправке'
