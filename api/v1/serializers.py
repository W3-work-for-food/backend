from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import User

from ambassadors.models import Ambassador, AmbassadorStatus, Content, Merch, SizedMerch, SentMerch



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


class AmbassadorStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmbassadorStatus
        fields = ['id', 'slug', 'status']


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'link', 'date', 'guide_condition']


class MerchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merch
        fields = ('__all__')
class AmbassadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambassador
        fields = ('__all__')

class SentMerchSerializer(serializers.ModelSerializer):
    merch = MerchSerializer(many=True)
    sized_merch = serializers.SerializerMethodField()
    ambassador = AmbassadorSerializer()
    user = UserSerializer()

    class Meta:
        model = SentMerch
        fields = ('id', 'user', 'date',
                  'ambassador', 'merch',
                  'amount', 'sized_merch',
                  'region_district'
        )


    def get_sized_merch(self, obj):
        query = obj.merch.all()
        ambassador = Ambassador.objects.get(id=obj.ambassador.id)
        ambassador_profile = ambassador.profile

        result = []
        for merch in query:
            match merch.category:
                case 'outerwear':
                    sized_merch = (merch.merch_type, ambassador_profile.clothing_size)
                case 'socks':
                    sized_merch = (merch.merch_type, ambassador_profile.foot_size)
                case _:
                    sized_merch = (merch.merch_type, None)
            result.append(sized_merch)
        return result

    def to_representation(self, instance):
        data = super().to_representation(instance)
        del data['merch']
        return data
