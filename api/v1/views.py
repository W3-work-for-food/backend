from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins, serializers, status, viewsets
from .serializers import UserSerializer, MerchSerializer
from ambassadors.models import Merch



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для пользователей"""
    
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user:
            return [self.request.user]
        return Response(status=status.HTTP_400_BAD_REQUEST)




class MerchViewSet(viewsets.ModelViewSet):
    """Вьюсет для пользователей"""
    
    permission_classes = [IsAuthenticated,]
    serializer_class = MerchSerializer
    queryset = Merch.objects.all()

