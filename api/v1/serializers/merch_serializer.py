from rest_framework import serializers

from ambassadors.models import Merch


class MerchSerializer(serializers.ModelSerializer):
    """Сериализатор мечра."""

    class Meta:
        model = Merch
        fields = '__all__'
