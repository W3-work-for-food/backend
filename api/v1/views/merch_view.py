from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ambassadors.models import Merch
from api.v1.serializers import MerchSerializer

MERCH_DESCRIPTION = 'Эндпоинты для создания, просмотра и отправки мерча'


@extend_schema(tags=['Мерч'], description=MERCH_DESCRIPTION)
class MerchViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для мерча."""
    permission_classes = [IsAuthenticated, ]
    serializer_class = MerchSerializer
    queryset = Merch.objects.all()
