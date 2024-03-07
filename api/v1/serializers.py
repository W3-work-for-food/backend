from django.db.models import Q
from rest_framework import serializers
from users.models import User
from ambassadors.models import (Ambassador, Promocode, Profile,
                                Address, AmbassadorStatus, Content, Merch)
from ambassadors.models import Ambassador, AmbassadorStatus, Content, Merch, SizedMerch, SentMerch


class ProfileSerializer(serializers.ModelSerializer):
    """
    Возвращает объекты модели Profile.
    """
    email = serializers.EmailField()

# TODO Надо доделать валидацию почты. Должен смотреть в базе и исключать текущего амба из неё
#     def validate_email(self, email):
#         if Ambassador.objects.filter(profile__email=email).exclude(id=self.instance.id).exists():
#             raise serializers.ValidationError(
#                 f'Пользователь с почтой {email} уже существует'
#             )
#         return email

    class Meta:
        model = Profile
        fields = ('id', 'email', 'gender', 'job', 'clothing_size', 'foot_size',
                  'blog_link', 'additional', 'education', 'education_path',
                  'education_goal', 'phone')
        read_only_fields = ('id',)


class AddressSerializer(serializers.ModelSerializer):
    """
    Возвращает объекты модели Address.
    """

    class Meta:
        model = Address
        fields = ('id', 'country', 'region', 'city', 'address', 'postal_code')
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
    promocodes = PromocodeSerializer(many=True, required=False, partial=True)
    address = AddressSerializer(required=True, partial=True)
    profile = ProfileSerializer(required=True, partial=True)

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

    def update(self, instance, validated_data):
        instance.telegram = validated_data.get('telegram', instance.telegram)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.guide_status = validated_data.get(
            'guide_status', instance.guide_status
        )

        new_address = validated_data.get('address')
        if new_address:
            address = instance.address
            for key, value in new_address.items():
                setattr(address, key, value)
            address.save()

        new_profile = validated_data.get('profile')
        if new_profile:
            profile = instance.profile
            for key, value in new_profile.items():
                setattr(profile, key, value)
            profile.save()

        new_codes = validated_data.get('promocodes')
        if new_codes:
            for code in new_codes:
                existing_promocode = Promocode.objects.filter(
                    Q(ambassador_id=instance.id) &
                    Q(promocode=code['promocode'])
                ).first()
                if existing_promocode:
                    existing_promocode.is_active = code['is_active']
                    existing_promocode.save()
                else:
                    Promocode(ambassador_id=instance.id, **code).save()
        else:
            Promocode.objects.filter(ambassador_id=instance.id).delete()
        instance.save()

        return instance

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
