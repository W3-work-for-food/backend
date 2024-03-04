from rest_framework import serializers

from notifications.models import Notification, NotificationStatus
from users.models import User


class NotificationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели уведомлений.
    Attributes:
        type (str): Тип уведомления.
        status (str): Статус уведомления.
        ambassador (str): Имя посла, связанного с уведомлением.
    Methods:
        update(instance, validated_data): Обновляет уведомление.
    Meta:
        model (Notification): Связанная модель уведомлений.
        fields (list): Список полей, включаемых в сериализацию.
        read_only_fields (list): Список полей, доступных только для чтения.
    """
    type = serializers.StringRelatedField()
    status = serializers.SlugRelatedField(slug_field='status', queryset=NotificationStatus.objects.all())
    ambassador = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ['id', 'pub_date', 'type', 'status', 'ambassador', ]
        read_only_fields = ['id', 'pub_date', 'type', 'ambassador', ]

    def update(self, instance, validated_data):
        status_data = validated_data.pop('status', None)
        if status_data is not None:
            status_obj = NotificationStatus.objects.get(status=status_data)
            instance.status = status_obj
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
