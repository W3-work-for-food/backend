from datetime import datetime
from http import HTTPMethod

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, views, viewsets
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from ambassadors.models import (
    Address, Ambassador, Content, Merch, Profile, Promocode, SentMerch
)
from ambassadors.models import Notification
from api.v1.serializers import (
    AddressSerializer, AmbassadorReadSerializer, AmbassadorWriteSerializer,
    ContentSerializer, MerchSerializer, ProfileSerializer,
    PromocodeSerializer, SentMerchSerializer, NotificationSerializer,
    UserSerializer
)
from .utils import read_notifications_for_month

AMBASSADORS_DESCRIPTION = (
    'Эндпоинты для создания, изменения и просмотра амбассадоров'
)
MERCH_DESCRIPTION = 'Эндпоинты для создания, просмотра и отправки мерча'
CONTENT_DESCRIPTION = 'Эндпоинты для создания и просмотра контента'
NOTIFICATION_DESCRIPTION = 'Эндпоинты для просмотра уведомлений'


@extend_schema(tags=['Авторизация'])
class UserAPIView(views.APIView):
    """Апивью для возврата текущего пользователя."""
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
    """Вьюсет для контента."""

    serializer_class = ContentSerializer
    queryset = Content.objects.all()

    def list(self, request, ambassador_id, *args, **kwargs):
        content = Content.objects.filter(ambassador_id=ambassador_id).all()
        print(content)
        serializer = ContentSerializer(content, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Мерч'], description=MERCH_DESCRIPTION)
class MerchViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для мерча."""
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
    """Вьюсет для амбассадоров."""
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
    """Вьюсет для отправки мерча."""
    permission_classes = [IsAuthenticated, ]
    serializer_class = SentMerchSerializer
    queryset = SentMerch.objects.all()

    def list(self, request, ambassador_id, *args, **kwargs):
        sent_merch = SentMerch.objects.filter(ambassador_id=ambassador_id)
        serializer = SentMerchSerializer(sent_merch, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

    def create(self, request, ambassador_id, *args, **kwargs):
        user = self.request.user
        
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

    @action(detail=False, methods=['get'])
    def budget(self, obj, ambassador_id):
        """Расчет бюджета на мерч по амбассадору."""
        print(ambassador_id)
        sent_merch_query = SentMerch.objects.filter(ambassador=ambassador_id)
        budget = sum([sent_merch.amount for sent_merch in sent_merch_query])
        return Response({'budget': budget}, status=status.HTTP_200_OK)

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
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PATCH":
        serializer = NotificationSerializer(notification, data=request.data,
                                            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

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


@extend_schema(tags=['Амбассадоры'], description=AMBASSADORS_DESCRIPTION)
@api_view(['POST'])
@permission_classes([AllowAny,])
def ambassadors_form_get(request):
    """
    Добавление амбассадоров через яндекс форму.
    """
    print('!!!!!', 'START')
    data = request.data
    # Профайл
    profile_data = data['profile']
    email = profile_data['email']
    gender = profile_data['gender']
    job = profile_data['job']
    clothing_size = profile_data['clothing_size']
    foot_size = profile_data['foot_size']
    blog_link = profile_data['blog_link']
    additional = profile_data['additional']
    education = profile_data['education']
    education_path = profile_data['education_path']
    education_goal = profile_data['education_goal']
    phone = profile_data['phone']
    print('!!!!!!!', 'enter')
    profile = Profile.objects.create(
        email=email,
        gender=gender,
        job=job,
        clothing_size=clothing_size,
        foot_size=foot_size,
        blog_link=blog_link,
        additional=additional,
        education=education,
        education_path=education_path,
        education_goal=education_goal,
        phone=phone,
    )
    print('!!!!!!!!!!', 'adress_start')
    address_data = data['address']
    country = address_data['country']
    region = address_data['region']
    city = address_data['city']
    address = address_data['address']
    postal_code = address_data['postal_code']
    address = Address.objects.create(
        country=country,
        region=region,
        city=city,
        address=address,
        postal_code=postal_code
    )

    telegram = data['telegram']
    name = data['name']
    pub_date=datetime.now()
    status = data['status']
    comment = data['comment']
    guide_status = data['guide_status']
    Ambassador.objects.get_or_create(
        telegram=telegram,
        defaults={
            'pub_date': pub_date,
            'name': name,
            'status': status,
            'comment': comment,
            'guide_status': guide_status,
            'address': address,
            'profile': profile,
        }
    )

    '''content_data = data['content']
    link = content_data['link']
    date = content_data['date']
    guide_condition = content_data['guide_condition']
    Content.objects.create(
        ambassador=ambassador,
                    link=link,
                    date=date,
                    guide_condition=guide_condition
                )'''
    print('!!!!!!!!', 'DONE')
    return Response(status=HTTP_200_OK)
