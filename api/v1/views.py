from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins, serializers, status, viewsets, views
from django.shortcuts import get_object_or_404

from ambassadors.models import AmbassadorStatus, Content, Merch, SentMerch, MerchBasket
from .serializers import (
    UserSerializer, MerchSerializer, MerchBasketSerializer,
    UserSerializer, AmbassadorStatusSerializer,
    ContentSerializer, SentMerchSerializer,
    CreateSentMerchSerializer,
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


class MerchBasketViewSet(viewsets.ModelViewSet):
    """Вьюсет для отправки мерча"""
    permission_classes = [IsAuthenticated,]
    serializer_class = MerchBasketSerializer
    queryset = MerchBasket.objects.all()
