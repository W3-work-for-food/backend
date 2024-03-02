from django.db import models
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


class Notification(models.Model):
    pass


class Profile(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
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
    blog_link = models.CharField(
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
    education_path = models.TextField(verbose_name='Путь обучения')


class Content(models.Model):
    pass


class Merch(models.Model):
    pass


class Promocode(models.Model):
    promocode = models.CharField(max_length=255, verbose_name='Промокод')
    is_active = models.BooleanField(verbose_name='Статус')


class AmbassadorStatus(models.Model):
    pass


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
    notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, verbose_name='Уведомления'
    )
    onboarding_date = models.DateTimeField(verbose_name='Дата онбординга')
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        verbose_name='Профиль'
    )
    ambassador_status = models.ForeignKey(
        AmbassadorStatus,
        on_delete=models.CASCADE,
        verbose_name='Статус амбассадора'
    )
    ambassador_address = models.ForeignKey(
        AmbassadorAddress,
        on_delete=models.CASCADE,
        verbose_name='Адрес амбассадора'
    )
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Контент'
    )
    merch = models.ForeignKey(
        Merch,
        on_delete=models.CASCADE,
        verbose_name='Мерч'
    )
    promocode = models.ForeignKey(
        Promocode,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name='Промокод'
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
