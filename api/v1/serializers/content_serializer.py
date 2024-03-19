from rest_framework import serializers

from ambassadors.models import Content


class ContentSerializer(serializers.ModelSerializer):
    """Сериализатор контентапользователя."""
    class Meta:
        model = Content
        fields = ['id', 'ambassador_id', 'link', 'date', 'guide_condition']
