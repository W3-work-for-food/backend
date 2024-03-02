import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


TGNAME_ERROR = ('Имя пользователя должно состоять из латинских букв,'
                ' цифр и символа нижнего подчеркивания, и быть длиной'
                ' от 5 до 32 символов')


def validate_tgname(value):
    """
    Проверяет корректность имени пользователя в Telegram.
    Начинаться с @ и состоять из латинских букв, может содержать цифры
    и нижнее подчеркивание, длина от 5 до 32 символов
    """
    if not re.match(r'^@[a-zA-Z0-9_]{5,32}$', value):
        raise ValidationError(_(f'{TGNAME_ERROR}'), params={'value': value})
