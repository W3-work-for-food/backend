from datetime import datetime
from http import HTTPMethod

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins, serializers, status, viewsets
from .serializers import (
    UserSerializer, AddressSerializer,
    AmbassadorReadSerializer,
    AmbassadorWriteSerializer, MerchSerializer, ProfileSerializer,
    PromocodeSerializer,
)
from ambassadors.models import Ambassador, Merch, Address, Profile, Promocode


class GetUserViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для текущего пользователя"""
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user:
            return [self.request.user]
        return Response(status=status.HTTP_400_BAD_REQUEST)


class MerchViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для мерча"""
    permission_classes = [IsAuthenticated,]
    serializer_class = MerchSerializer
    queryset = Merch.objects.all()


class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class PromocodeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = PromocodeSerializer
    queryset = Promocode.objects.all()


class AmbassadorsViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    """
    Вьюха для создания/просмотра амбассадоров
    """
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated, ]
    queryset = Ambassador.objects.all()

    def get_serializer_class(self):
        if self.request.method == HTTPMethod.POST:
            return AmbassadorWriteSerializer
        return AmbassadorReadSerializer

    def perform_create(self, serializer):
        serializer.save(pub_date=datetime.now())
