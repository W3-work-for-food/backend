from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class NotificationStatusSerializer(serializers.ModelSerializer):
    """Возвращает объекты модели StatusIDP"""

    class Meta:
        model = None  # StatusNotification
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    """Возвращает объект конкретного уведомления"""
    status = NotificationStatusSerializer()

    class Meta:
        model = None  # Notification
        fields = (
            'id',
            'ambassador',
            'date',
            'type',
            'status',
        )