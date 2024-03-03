from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins, serializers, status, viewsets

from ambassadors.models import AmbassadorStatus, Content, Merch
from .serializers import (
    UserSerializer, MerchSerializer,
    UserSerializer, AmbassadorStatusSerializer,
    ContentSerializer
)

class GetUserViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для текущего пользователя"""
    permission_classes = [IsAuthenticated,]
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
    permission_classes = [IsAuthenticated,]
    serializer_class = MerchSerializer
    queryset = Merch.objects.all()
