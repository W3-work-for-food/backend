from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response

from ambassadors.models import Content
from api.v1.serializers import ContentSerializer

CONTENT_DESCRIPTION = 'Эндпоинты для создания и просмотра контента'


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
    