from rest_framework import serializers

from ambassadors.models import Promocode


class PromocodeSerializer(serializers.ModelSerializer):
    """
    Возвращает объекты модели Promocode.
    """

    class Meta:
        model = Promocode
        fields = ('id', 'promocode', 'is_active')
        read_only_fields = ('id',)
