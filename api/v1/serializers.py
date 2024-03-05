from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import User

from ambassadors.models import AmbassadorStatus, Content, Merch, SizedMerch, SentMerch, MerchBasket



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
        fields = ('id', 'merch_type', 'category', 'price')

class SentMerchSerializer(serializers.ModelSerializer):
    merch = MerchSerializer(many=True, read_only=True)
    budget = serializers.SerializerMethodField()
    sized_merch = serializers.SerializerMethodField()
    
    class Meta:
        model = SentMerch
        fields = ('id', 'user', 'ambassador', 'merch', 'budget', 'sized_merch')

    def get_budget(self, obj):
        query = obj.merch.all()
        budget = sum([merch.price for merch in query])
        return budget

    def get_sized_merch(self, obj):
        query = obj.merch.all()
        ambassador_profile = obj.ambassador.profile
        result = []
        for merch in query:
            match merch.category:
                case 'outerwear':
                    sized_merch = (merch.merch_type, ambassador_profile.clothing_size)
                case 'socks':
                    sized_merch = (merch.merch_type, ambassador_profile.foot_size)
                case _:
                    sized_merch = (merch.merch_type,)
            result.append(sized_merch)
        return result

class CreateSentMerchSerializer(serializers.ModelSerializer):
    #merch = MerchSerializer(many=True, read_only=True)
    budget = serializers.SerializerMethodField()
    sized_merch = serializers.SerializerMethodField()

    class Meta:
        model = SentMerch
        fields = ('id', 'user', 'ambassador', 'merch', 'budget', 'sized_merch')

class MerchBasketSerializer(serializers.ModelSerializer):
    
    merch = MerchSerializer(many=True, read_only=True)
    budget = serializers.SerializerMethodField()
    
    class Meta:
        model = MerchBasket
        fields = ('id', 'merch', 'budget')

    def get_budget(self, obj):
        query = obj.merch.all()
        budget = sum([merch.price for merch in query])
        return budget
