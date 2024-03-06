from rest_framework import serializers
from users.models import User
from ambassadors.models import (Ambassador, Promocode, Profile,
                                Address, AmbassadorStatus, Content, Merch)


class ProfileSerializer(serializers.ModelSerializer):
    """
    Возвращает объекты модели Profile.
    """

    class Meta:
        model = Profile
        fields = ('id', 'email', 'gender', 'job', 'clothing_size', 'foot_size',
                  'blog_link', 'additional', 'education', 'education_path',
                  'education_goal', 'phone')


class AddressSerializer(serializers.ModelSerializer):
    """
    Возвращает объекты модели Address.
    """

    class Meta:
        model = Address
        fields = ('id', 'country', 'city', 'address', 'postal_code')
        read_only_fields = ('id',)


class PromocodeSerializer(serializers.ModelSerializer):
    """
    Возвращает объекты модели Promocode.
    """

    class Meta:
        model = Promocode
        fields = ('id', 'promocode', 'is_active')


class AmbassadorReadSerializer(serializers.ModelSerializer):
    """
    Возвращает объекты модели Ambassadors.
    """
    promocodes = PromocodeSerializer(many=True, required=False)
    address = AddressSerializer()
    profile = ProfileSerializer()

    def get_promocodes(self, ambassador):
        promocodes = Promocode.objects.filter(ambassador_id=ambassador.id)
        serializer = PromocodeSerializer(promocodes, many=True)
        return serializer.data

    class Meta:
        model = Ambassador
        fields = ('id', 'pub_date', 'telegram', 'name', 'profile',
                  'address', 'promocodes', 'comment', 'guide_status')
        read_only_fields = ('id', 'pub_date', 'telegram', 'name', 'profile',
                            'address', 'promocodes', 'comment', 'guide_status')


class AmbassadorWriteSerializer(serializers.ModelSerializer):
    """
    Возвращает объекты модели Ambassadors.
    """
    promocodes = PromocodeSerializer(many=True, required=False)
    address = AddressSerializer(many=False, required=True)
    profile = ProfileSerializer(many=False, required=True)

    def create(self, validated_data):
        promocodes_data = validated_data.pop('promocodes')
        address_data = validated_data.pop('address')
        profile_data = validated_data.pop('profile')

        address_serializer = AddressSerializer(data=address_data)
        if address_serializer.is_valid():
            address = address_serializer.save()

        profile_serializer = ProfileSerializer(data=profile_data)
        if profile_serializer.is_valid():
            profile = profile_serializer.save()

        ambassador = Ambassador.objects.create(
            address_id=address.id,
            profile_id=profile.id,
            **validated_data
        )

        promocodes = [
            Promocode.objects.create(
                ambassador_id=ambassador.id,
                **promo_code
            ) for promo_code in promocodes_data
        ]

        ambassador_data = self.to_representation(ambassador)
        ambassador_data['promocodes'] = PromocodeSerializer(
            promocodes, many=True
        ).data

        return ambassador_data

    class Meta:
        model = Ambassador
        fields = ('id', 'pub_date', 'telegram', 'name', 'profile',
                  'address', 'promocodes', 'comment', 'guide_status')
        read_only_fields = ('id', 'pub_date')


# class NotificationStatusSerializer(serializers.ModelSerializer):
#     """Возвращает объекты модели StatusIDP"""
#
#     class Meta:
#         model = None  # StatusNotification
#         fields = '__all__'


# class NotificationSerializer(serializers.ModelSerializer):
#     """Возвращает объект конкретного уведомления"""
#     status = NotificationStatusSerializer()
#
#     class Meta:
#         model = None  # Notification
#         fields = (
#             'id',
#             'ambassador',
#             'date',
#             'type',
#             'status',
#         )


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
        fields = ('merch_type', 'category', 'price')
