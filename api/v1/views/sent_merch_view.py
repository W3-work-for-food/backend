from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ambassadors.models import SentMerch, Ambassador, Merch
from api.v1.serializers import SentMerchSerializer

MERCH_DESCRIPTION = 'Эндпоинты для создания, просмотра и отправки мерча'


@extend_schema(tags=['Мерч'], description=MERCH_DESCRIPTION)
class SentMerchViewSet(viewsets.ModelViewSet):
    """Вьюсет для отправки мерча."""
    permission_classes = [IsAuthenticated, ]
    serializer_class = SentMerchSerializer
    queryset = SentMerch.objects.all()

    def list(self, request, ambassador_id, *args, **kwargs):
        sent_merch = SentMerch.objects.filter(ambassador_id=ambassador_id)
        serializer = SentMerchSerializer(sent_merch, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, ambassador_id, *args, **kwargs):
        user = self.request.user
        ambassador = get_object_or_404(Ambassador, id=ambassador_id)
        merch_id_list = request.data['merch']

        sent_merch = SentMerch.objects.create(user=user, ambassador=ambassador)
        lst = []
        amount = 0

        for merch_id in merch_id_list:
            merch = get_object_or_404(Merch, id=merch_id)
            amount += merch.price
            lst.append(merch.id)
        sent_merch.merch.set(lst)
        sent_merch.amount = amount
        sent_merch.save()
        serializer = SentMerchSerializer(sent_merch)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def budget(self, obj, ambassador_id):
        """Расчет бюджета на мерч по амбассадору."""
        sent_merch_query = SentMerch.objects.filter(ambassador=ambassador_id)
        budget = sum([sent_merch.amount for sent_merch in sent_merch_query])
        return Response({'budget': budget}, status=status.HTTP_200_OK)
