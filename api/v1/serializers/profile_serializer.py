from rest_framework import serializers

from ambassadors.models import Profile


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
        read_only_fields = ('id', )
