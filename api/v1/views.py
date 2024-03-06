from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins, serializers, status, viewsets, views
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from ambassadors.models import Ambassador, AmbassadorStatus, Content, Merch, SentMerch
from .serializers import (
    UserSerializer, MerchSerializer, 
    UserSerializer, AmbassadorStatusSerializer,
    ContentSerializer, SentMerchSerializer,
)


class UserAPIView(views.APIView):
    """Вьюсет для текущего пользователя"""
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer
    
    def get(self, request, format=None):
        if self.request.user:
            serializer = UserSerializer(self.request.user)
            return Response(
                data=serializer.data, status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AmbassadorStatusView(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для статусов амбассадоров"""

    serializer_class = AmbassadorStatusSerializer
    queryset = AmbassadorStatus.objects.all()


class ContentViewSet(viewsets.ModelViewSet):
    """Вьюсет для контента"""

    serializer_class = ContentSerializer
    queryset = Content.objects.all()


class MerchViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для мерча"""
    permission_classes = [IsAuthenticated,]
    serializer_class = MerchSerializer
    queryset = Merch.objects.all()


class SentMerchViewSet(viewsets.ModelViewSet):
    """Вьюсет для отправки мерча"""
    permission_classes = [IsAuthenticated,]
    serializer_class = SentMerchSerializer
    queryset = SentMerch.objects.all()

    def create(self, request, *args, **kwargs):
        user = self.request.user
        ambassador_id = request.data['ambassador']
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
        if 'region_district' in request.data:
            sent_merch.region_district = request.data['region_district']
        sent_merch.save()
        serializer = SentMerchSerializer(sent_merch)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


    @action(
        detail=False,
        methods=['post'],
    )
    def budget(self, obj):
        """Расчет бюджета на мерч"""
        ambassador_id = self.request.data['ambassador']
        sent_merch_query = SentMerch.objects.filter(ambassador=ambassador_id)
        budget = sum([sent_merch.amount for sent_merch in sent_merch_query])
        return Response({'budget':budget}, status=status.HTTP_200_OK)

