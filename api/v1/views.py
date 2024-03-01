from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins, serializers, status, viewsets
from ambassadors.models import AmbassadorStatus, Content
from .serializers import (
    UserSerializer,
    AmbassadorStatusSerializer,
    ContentSerializer
)



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для пользователей"""

    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user:
            return [self.request.user]
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AmbassadorStatusView(viewsets.ModelViewSet):
    """Вьюсет для статусов амбассадоров"""

    serializer_class = AmbassadorStatusSerializer
    queryset = AmbassadorStatus.objects.all()


class ContentView(viewsets.ModelViewSet):
    """Вьюсет для контента"""

    serializer_class = ContentSerializer
    queryset = Content.objects.all()
