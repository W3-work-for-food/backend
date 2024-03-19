from drf_spectacular.utils import extend_schema
from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.serializers import UserSerializer


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
