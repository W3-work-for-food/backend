from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import User


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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')



class MerchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'category', 'size', 'price')
