
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins, serializers, status, viewsets
from .serializers import UserSerializer
from users.models import User
from django.shortcuts import get_object_or_404



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для пользователей"""
    
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user:
            return [self.request.user]
        return Response(status=status.HTTP_400_BAD_REQUEST)
