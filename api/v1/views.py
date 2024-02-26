from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

    @action(detail=False, methods=['get'])
    def viewed(self, request, *args, **kwargs):
        """
        Возвращает список прочитанных уведомлений.
        Временная заглушка пока что.
        """
        viewed_notifications = self.queryset.filter(status='Прочитано')
        serializer = self.get_serializer(viewed_notifications, many=True)
        return Response(serializer.data)
