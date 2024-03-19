from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ambassadors.models import Address
from api.v1.serializers import AddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    """Вьюсет для адреса."""
    permission_classes = [IsAuthenticated, ]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
