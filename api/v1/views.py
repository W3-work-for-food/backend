from rest_framework import status, viewsets, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.serializers import NotificationSerializer
from api.v1.utils import read_notifications_for_month
from notifications.models import Notification

from ambassadors.models import AmbassadorStatus, Content, Merch
from .serializers import (
    MerchSerializer,
    UserSerializer, AmbassadorStatusSerializer,
    ContentSerializer
)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def notification_detail(request, pk):
    """
    Получение и обновление уведомления по его идентификатору.
    Args:
        request (HttpRequest): Объект запроса.
        pk (int): Идентификатор уведомления.
    Returns:
        Response: HTTP-ответ с данными уведомления или ошибкой.
    """
    notification = Notification.objects.get(pk=pk)

    if request.method == "GET":
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PATCH":
        serializer = NotificationSerializer(notification, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_list(request, status):
    """
    Получение списка уведомлений по статусу, типу и дате.
    Args:
        request (HttpRequest): Объект запроса.
        status (str): Статус уведомлений ("Непрочитано" или "Прочитано").
    Returns:
        Response: HTTP-ответ со списком уведомлений или ошибкой.
    """
    type = request.query_params.get('type')
    date_from = request.query_params.get('pub_date')
    date_to = request.query_params.get('pub_date')

    notifications = Notification.objects.filter(status__status=status)

    match status:
        case 'Непрочитано':
            if type:
                notifications = notifications.filter(type=type)
            if date_from and date_to:
                notifications = notifications.filter(
                    date__range=(date_from, date_to)
                )
        case 'Прочитано':
            last_month_start, last_month_end = read_notifications_for_month()
            notifications = notifications.filter(pub_date__range=(last_month_start, last_month_end))

    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data, 200)


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
