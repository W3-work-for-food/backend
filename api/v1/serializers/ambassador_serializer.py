from django.db.models import Q
from rest_framework import serializers

from ambassadors.models import Promocode, Ambassador, Notification
from api.v1.serializers import address_serializer as address_s
from api.v1.serializers import profile_serializer as profile_s
from api.v1.serializers import promocode_serializer as promocode_s

ERR_EMAIL_MSG = 'Амбассадор с почтой {} уже существует'
ERR_PROMO_MSG = 'Промокод {} уже существует'
ERR_TG_MSG = 'Амбассадор с телеграмом {} уже существует'


class AmbassadorReadSerializer(serializers.ModelSerializer):
    """
    Возвращает объекты модели Ambassadors.
    """
    promocodes = promocode_s.PromocodeSerializer(many=True)
    address = address_s.AddressSerializer()
    profile = profile_s.ProfileSerializer()

    def get_promocodes(self, ambassador):
        promocodes = Promocode.objects.filter(ambassador_id=ambassador.id)
        serializer = promocode_s.PromocodeSerializer(promocodes, many=True)
        return serializer.data

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
    promocodes = promocode_s.PromocodeSerializer(many=True, partial=True)
    address = address_s.AddressSerializer(partial=True)
    profile = profile_s.ProfileSerializer(partial=True)

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

        address_serializer = address_s.AddressSerializer(data=address_data)
        if address_serializer.is_valid():
            address = address_serializer.save()

        profile_serializer = profile_s.ProfileSerializer(data=profile_data)
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
        ambassador_data['promocodes'] = promocode_s.PromocodeSerializer(
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

