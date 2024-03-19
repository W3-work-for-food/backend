from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ambassadors.models import Profile
from api.v1.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """Вьюсет для профайла."""
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
