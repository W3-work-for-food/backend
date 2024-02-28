from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Неверный логин или пароль'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({'message': 'Вы вышли из системы'})
    else:
        return Response({'error': 'Пользователь не авторизован'}, status=401)
