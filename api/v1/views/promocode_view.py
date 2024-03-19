from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ambassadors.models import Promocode
from api.v1.serializers import PromocodeSerializer


class PromocodeViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для промокодов."""
    permission_classes = [IsAuthenticated, ]
    serializer_class = PromocodeSerializer
    queryset = Promocode.objects.all()
