from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_405_METHOD_NOT_ALLOWED

from ambassadors.models import Notification
from api.v1.serializers import NotificationSerializer
from api.v1.utils import read_notifications_for_month

NOTIFICATION_DESCRIPTION = 'Эндпоинты для просмотра уведомлений'


@extend_schema(tags=['Уведомления'], description=NOTIFICATION_DESCRIPTION)
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def notification_detail(request, pk):
    """
    Получение и обновление уведомления по его идентификатору.
    """
    notification = Notification.objects.get(pk=pk)

    if request.method == "GET":
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=HTTP_200_OK)

    elif request.method == "PATCH":
        serializer = NotificationSerializer(notification, data=request.data,
                                            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)
    return Response(status=HTTP_405_METHOD_NOT_ALLOWED)


@extend_schema(tags=['Уведомления'], description=NOTIFICATION_DESCRIPTION)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_list(request, status):
    """
    Получение списка уведомлений по статусу, типу и дате.
    """
    type = request.query_params.get('type')
    date_from = request.query_params.get('pub_date')
    date_to = request.query_params.get('pub_date')

    notifications = Notification.objects.filter(status=status)

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
            notifications = notifications.filter(
                pub_date__range=(last_month_start, last_month_end))

    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data, status=HTTP_200_OK)
