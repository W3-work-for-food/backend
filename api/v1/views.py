from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from api.v1.serializers import NotificationSerializer


class NotificationViewSet(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    Заглушка.
    """
    # queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'date']

    @action(detail=False, methods=['get'])
    def viewed(self, request, *args, **kwargs):
        """
        Возвращает список прочитанных уведомлений.
        Временная заглушка пока что.
        """
        viewed_notifications = self.queryset.filter(status='прочитано')
        serializer = self.get_serializer(viewed_notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def unviewed(self, request, *args, **kwargs):
        """
        Возвращает список непрочитанных уведомлений.
        Временная заглушка пока что.
        """
        viewed_notifications = self.queryset.filter(status='непрочитано')
        serializer = self.get_serializer(viewed_notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
