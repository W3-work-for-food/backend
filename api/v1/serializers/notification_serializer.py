from rest_framework import serializers

from ambassadors.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели уведомлений.
    """
    ambassador = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'pub_date', 'type', 'status', 'ambassador', ]
        read_only_fields = ['id', 'pub_date', 'type', 'ambassador', ]

    def get_ambassador(self, value):
        data = {
            'ambassador_id': value.ambassador.id,
            'telegram': value.ambassador.telegram,
            'name': value.ambassador.name
        }
        return data
