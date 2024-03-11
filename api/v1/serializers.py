from django.db.models import Q
from rest_framework import serializers

from ambassadors.models import (CLOTHING_SIZE_CHOICES, GENDER_CHOICES, Address,
                                Ambassador, Content, Merch, Notification,
                                Profile, Promocode, SentMerch)
from users.models import User

ERR_EMAIL_MSG = 'Амбассадор с почтой {} уже существует'
ERR_PROMO_MSG = 'Промокод {} уже существует'
ERR_TG_MSG = 'Амбассадор с телеграмом {} уже существует'


class ProfileSerializer(serializers.ModelSerializer):
    """
    Возвращает объекты модели Profile.
    """

    class Meta:
        model = Profile
        fields = (
            'id', 'email', 'gender', 'job', 'clothing_size', 'foot_size',
            'blog_link', 'additional', 'education', 'education_path',
            'education_goal', 'phone'
        )
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
    promocodes = PromocodeSerializer(many=True)
    address = AddressSerializer()
    profile = ProfileSerializer()

    def get_promocodes(self, ambassador):
        promocodes = Promocode.objects.filter(ambassador_id=ambassador.id)
        serializer = PromocodeSerializer(promocodes, many=True)
        return serializer.data

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Ambassador
        fields = (
            'id', 'pub_date', 'telegram', 'name', 'profile', 'address',
            'promocodes', 'comment', 'guide_status', 'status'
        )
        read_only_fields = (
            'id', 'pub_date', 'telegram', 'name', 'profile', 'address',
            'promocodes', 'comment', 'guide_status', 'status'
        )


class AmbassadorWriteSerializer(serializers.ModelSerializer):
    """
    Возвращает объекты модели Ambassadors.
    """
    promocodes = PromocodeSerializer(many=True, partial=True)
    address = AddressSerializer(partial=True)
    profile = ProfileSerializer(partial=True)

    def validate_profile(self, attrs):
        ambassador_id = self.instance.id if self.instance else None
        email = attrs.get('email')

        if ambassador_id:
            if Ambassador.objects.filter(profile__email=email).exclude(
                    id=ambassador_id
            ).exists():
                raise serializers.ValidationError(ERR_EMAIL_MSG.format(email))
            return attrs

        if Ambassador.objects.filter(profile__email=email).exists():
            raise serializers.ValidationError(ERR_EMAIL_MSG.format(email))

        return attrs

    def validate_promocodes(self, promocodes):
        ambassador_id = self.instance.id if self.instance else None

        if ambassador_id:
            for code in promocodes:
                if Promocode.objects.filter(
                        promocode=code['promocode']).exclude(
                        ambassador_id=ambassador_id
                ).exists():
                    raise serializers.ValidationError(
                        ERR_PROMO_MSG.format(code['promocode'])
                    )
            return promocodes

        for code in promocodes:
            if Promocode.objects.filter(promocode=code['promocode']).exists():
                raise serializers.ValidationError(
                    ERR_PROMO_MSG.format(code['promocode'])
                )

        return promocodes

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
            address_id=address.id,  # NOQA
            profile_id=profile.id,  # NOQA
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

        notification = Notification.objects.create(
            ambassador=ambassador, type='new_profile',
            status='unread'
        )
        notification.save()
        return ambassador_data

    def update(self, instance, validated_data):
        instance.telegram = validated_data.get('telegram', instance.telegram)
        instance.name = validated_data.get('name', instance.name)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.status = validated_data.get('status', instance.status)

        if instance.guide_status is False and validated_data.get(
            'guide_status'
        ) is True:
            Notification.objects.create(
                ambassador_id=instance.id, type='guide_completed',
                status='unread'
            )
        instance.guide_status = validated_data.get(
            'guide_status', instance.guide_status
        )

        new_address = validated_data.get('address')
        new_promo_codes = validated_data.get('promocodes')
        new_profile = validated_data.get('profile')

        if new_address:
            address = instance.address
            for key, value in new_address.items():
                setattr(address, key, value)
            address.save()

        if new_profile:
            profile = instance.profile
            for key, value in new_profile.items():
                setattr(profile, key, value)
            profile.save()

        if new_promo_codes:
            for code_obj in new_promo_codes:
                existing_promo_code = Promocode.objects.filter(
                    Q(ambassador_id=instance.id) &
                    Q(promocode=code_obj['promocode'])
                ).first()
                if (
                    existing_promo_code and
                    existing_promo_code.is_active != code_obj['is_active']
                ):
                    existing_promo_code.is_active = code_obj['is_active']
                    existing_promo_code.save()
                else:
                    Promocode(ambassador_id=instance.id, **code_obj).save()
        else:
            Promocode.objects.filter(ambassador_id=instance.id).delete()
        instance.save()

        return instance

    class Meta:
        model = Ambassador
        fields = (
            'id', 'pub_date', 'telegram', 'name', 'profile', 'address',
            'promocodes', 'content', 'comment', 'guide_status', 'status'
        )
        read_only_fields = ('id', 'pub_date')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ContentSerializer(serializers.ModelSerializer):
    """Сериализатор контентапользователя."""
    class Meta:
        model = Content
        fields = ['id', 'ambassador_id', 'link', 'date', 'guide_condition']


class MerchSerializer(serializers.ModelSerializer):
    """Сериализатор мечра."""
    class Meta:
        model = Merch
        fields = '__all__'


class AmbassadorSerializer(serializers.ModelSerializer):
    """Сериализатор амбассадора."""
    class Meta:
        model = Ambassador
        fields = '__all__'


class SentMerchSerializer(serializers.ModelSerializer):
    """Сериализатор отправки мерча."""
    merch = MerchSerializer(many=True)
    sized_merch = serializers.SerializerMethodField()
    ambassador = AmbassadorSerializer()
    user = UserSerializer()

    class Meta:
        model = SentMerch
        fields = (
            'id', 'user', 'date', 'ambassador', 'merch', 'amount',
            'sized_merch',
        )

    def get_sized_merch(self, obj):
        query = obj.merch.all()
        ambassador = Ambassador.objects.get(id=obj.ambassador.id)
        ambassador_profile = ambassador.profile

        result = []
        for merch in query:
            match merch.category:
                case 'outerwear':
                    sized_merch = (
                        merch.merch_type, ambassador_profile.clothing_size
                    )
                case 'socks':
                    sized_merch = (
                        merch.merch_type, ambassador_profile.foot_size
                    )
                case _:
                    sized_merch = (merch.merch_type, None)
            result.append(sized_merch)
        return result


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
