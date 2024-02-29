from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class CustomAuthTokenSerializer(serializers.Serializer):
    """Кастомный сериализатор аутентификации."""
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = _('Не удается войти в систему с предоставленными учетными данными.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Должны быть указаны "E-mail" и "пароль".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class CustomObtainAuthToken(ObtainAuthToken):
    """Кастомный класс аутентификации."""
    serializer_class = CustomAuthTokenSerializer
