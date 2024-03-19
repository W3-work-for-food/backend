from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        read_only_fields = ('first_name', 'last_name')
