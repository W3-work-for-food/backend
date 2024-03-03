from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import UserViewSet, notification_detail, notification_list

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('notifications/<int:pk>/', notification_detail, name="notification-detail"),
    path('notifications/unviewed/', notification_list, {'status': 'Непрочитано'}, name='notification-unviewed-list'),
    path('notifications/viewed/', notification_list, {'status': 'Прочитано'}, name='notification-viewed-list'),
]

