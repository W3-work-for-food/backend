from datetime import datetime
from http import HTTPMethod

from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ambassadors.models import Ambassador, Merch, Address, Profile, Promocode, AmbassadorStatus, Content
from .serializers import (
    UserSerializer, AddressSerializer, AmbassadorReadSerializer,
    AmbassadorWriteSerializer, MerchSerializer, ProfileSerializer,
    PromocodeSerializer, AmbassadorStatusSerializer, ContentSerializer
)

AMBASSADORS_DESCRIPTION = ('Ендпоинты для создания, изменения и просмотра '
                           'амбассадоров')


class GetUserViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для текущего пользователя"""
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user:
            return [self.request.user]
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
    permission_classes = [IsAuthenticated, ]
    serializer_class = MerchSerializer
    queryset = Merch.objects.all()


class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class PromocodeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PromocodeSerializer
    queryset = Promocode.objects.all()


@extend_schema(tags=['Амбассадоры'], description=AMBASSADORS_DESCRIPTION)
class AmbassadorsViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin
):
    http_method_names = ['get', 'post', 'patch']
    permission_classes = [IsAuthenticated, ]
    queryset = Ambassador.objects.all()

    def get_serializer_class(self):
        match self.request.method:
            case HTTPMethod.GET:
                return AmbassadorReadSerializer
            case HTTPMethod.POST | HTTPMethod.PATCH:
                return AmbassadorWriteSerializer

    def perform_create(self, serializer):
        serializer.save(pub_date=datetime.now())
