from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet

router_v1 = DefaultRouter()
router_v1.register(r'notifications', NotificationViewSet, basename='notifications')

urlpatterns = [
    path('', include(router_v1.urls)),
]
