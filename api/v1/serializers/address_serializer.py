from rest_framework import serializers

from ambassadors.models import Address


class AddressSerializer(serializers.ModelSerializer):
    """
    Возвращает объекты модели Address.
    """

    class Meta:
        model = Address
        fields = ('id', 'country', 'region', 'city', 'address', 'postal_code')
        read_only_fields = ('id',)
