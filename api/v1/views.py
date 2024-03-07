from datetime import datetime
from http import HTTPMethod

from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .utils import read_notifications_for_month
from ambassadors.models import (Address, Ambassador, Content, Merch, Profile,
                                Promocode, SentMerch)
from api.v1.serializers import (AddressSerializer, AmbassadorReadSerializer,
                                AmbassadorWriteSerializer, ContentSerializer,
                                MerchSerializer, ProfileSerializer,
                                PromocodeSerializer, SentMerchSerializer,
                                NotificationSerializer, UserSerializer)
from ambassadors.models import Notification

AMBASSADORS_DESCRIPTION = ('Эндпоинты для создания, изменения и просмотра '
                           'амбассадоров')
MERCH_DESCRIPTION = ('Эндпоинты для создания и просмотра отправки мерча и'
                        'просмотра мерча и ')
CONTENT_DESCRIPTION = ('Эндпоинты для создания и просмотра контента')


class UserAPIView(views.APIView):
    """Апивью для возврата текущего пользователя"""
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializer

    def get(self, request, format=None):
        if self.request.user:
            serializer = UserSerializer(self.request.user)
            return Response(
                data=serializer.data, status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Контент'], description=CONTENT_DESCRIPTION)
class ContentViewSet(viewsets.ModelViewSet):
    """Вьюсет для контента"""

    serializer_class = ContentSerializer
    queryset = Content.objects.all()

@extend_schema(tags=['Мерч'], description=MERCH_DESCRIPTION)
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


@extend_schema(tags=['Мерч'], description=MERCH_DESCRIPTION)
class SentMerchViewSet(viewsets.ModelViewSet):
    """Вьюсет для отправки мерча"""
    permission_classes = [IsAuthenticated, ]
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
        return Response({'budget': budget}, status=status.HTTP_200_OK)

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