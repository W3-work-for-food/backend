from django.db import models
from django.db import models
from users.models import User
from ambassadors.validators import validate_tg_name


# TODO: Добавить к Шамилю в модель  в поле статус
STATUS_CHOICES = (
    ('active', 'Активный'),
    ('paused', 'На паузе'),
    ('non_ambassador', 'Не амбассадор'),
    ('clarifying', 'Уточняется'),
)

GENDER_CHOICES = (('male', 'М'), ('female', 'Ж'))

CLOTHING_SIZE_CHOICES = [
    ('extra_small', 'XS'),
    ('small', 'S'),
    ('medium', 'M'),
    ('large', 'L'),
    ('extra_large', 'XL'),
]

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
        verbose_name='Стоимость единицы',
    )

    class Meta:
        verbose_name = 'Мерч'
        verbose_name_plural = 'Мерч'


    def __str__(self):
        return f'{self.merch_type}'

class Notification(models.Model):
    pass


class Profile(models.Model):
    '''email = models.EmailField(unique=True, verbose_name='Email')
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, verbose_name='Пол'
    )
    job = models.CharField(max_length=255, verbose_name='Работа')'''
    clothing_size = models.CharField(
        max_length=11,
        choices=CLOTHING_SIZE_CHOICES,
        verbose_name='Размер одежды'
    )
    foot_size = models.IntegerField(verbose_name='Размер обуви')
    '''blog_link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Ссылка на блог'
    )
    additional = models.TextField(
        max_length=1024,
        blank=True,
        null=True,
        verbose_name='Дополнительная информация')
    education_path = models.TextField(verbose_name='Путь обучения')'''


class Content(models.Model):
    link = models.URLField(max_length=255, unique=False, blank=False)
    date = models.DateTimeField(
        max_length=30,
        auto_now_add=True,
        unique=False,
        blank=False
    )
    guide_condition = models.BooleanField(unique=False, blank=False)


class Promocode(models.Model):
    promocode = models.CharField(max_length=255, verbose_name='Промокод')
    is_active = models.BooleanField(verbose_name='Статус')


class AmbassadorStatus(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.status


class AmbassadorAddress(models.Model):
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    country = models.CharField(max_length=255, verbose_name='Страна')
    city = models.CharField(max_length=255, verbose_name='Город')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    postal_code = models.CharField(
        max_length=255,
        verbose_name='Почтовый индекс'
    )
    education = models.TextField(verbose_name='Образование')
    education_goal = models.TextField(verbose_name='Цель обучения')
    phone = models.CharField(max_length=255, verbose_name='Телефон')


class Ambassador(models.Model):
    telegram = models.CharField(
        max_length=35,
        validators=[validate_tg_name],
        unique=True,
        verbose_name='Телеграм'
    )
    name = models.CharField(max_length=255, verbose_name='ФИО')
    '''notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, verbose_name='Уведомления',
        blank=True#
    )'''
    onboarding_date = models.DateTimeField(verbose_name='Дата онбординга')
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        verbose_name='Профиль',
        blank=True#
    )
    '''ambassador_status = models.ForeignKey(
        AmbassadorStatus,
        on_delete=models.CASCADE,
        verbose_name='Статус амбассадора',
        blank=True#
    )'''
    '''ambassador_address = models.ForeignKey(
        AmbassadorAddress,
        on_delete=models.CASCADE,
        verbose_name='Адрес амбассадора',
        blank=True#
    )'''
    '''content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Контент'
    )'''
    '''merch = models.ForeignKey(
        Merch,
        on_delete=models.CASCADE,
        verbose_name='Мерч',
        blank=True#
    )'''
    '''promocode = models.ForeignKey(
        Promocode,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name='Промокод'
    )'''
    comment = models.TextField(
        max_length=1024,
        blank=True,
        verbose_name='Комментарий'
    )
    guide_status = models.BooleanField(
        default=False,
        verbose_name='Статус гайда'
    )


class SizedMerch(models.Model):
    merch = models.ForeignKey(
        Merch,
        on_delete=models.CASCADE,
        verbose_name='Мерч',
    )
    size = models.CharField(
        max_length=11,
        verbose_name='Размер мерча'
    )

class SentMerch(models.Model):
    """Модель мерч в отправке"""
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
    region_district = models.CharField(
        max_length=254,
        verbose_name='Область/район',
        blank=True, null=True
    )
