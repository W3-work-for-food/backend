import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


TG_NAME_ERROR = ('Имя пользователя должно начинать с символа "@" и состоять из'
                ' латинских букв, цифр и символа нижнего подчеркивания, и быть'
                ' длиной от 5 до 32 символов')

PROMO_CODE_ERROR = 'Промокод должен состоять из латинских букв, цифр'


def validate_tg_name(value):
    """
    Проверяет корректность имени пользователя в Telegram.
    """
    if not re.match(r'^@[a-zA-Z0-9_]{5,32}$', value):
        raise ValidationError(_(f'{TG_NAME_ERROR}'), params={'value': value})


def validate_promo_code(value):
    if not re.match(r'^[a-zA-Z0-9]{5,100}$', value):
        raise ValidationError(_(f'{PROMO_CODE_ERROR}'), params={'value': value})
