from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    notification_detail,
    notification_list,
    ContentViewSet,
    AmbassadorStatusView,
    GetUserViewSet,
    MerchViewSet,
)
router = DefaultRouter()
router.register('content', ContentViewSet, basename='content')
router.register(
    'ambassador_status',
    AmbassadorStatusView,
    basename='ambassador_status'
)
router.register('getusers', GetUserViewSet, basename='getusers')
router.register('merch', MerchViewSet, basename='merch')

urlpatterns = [
    path('', include(router.urls)),
    path('notifications/<int:pk>/', notification_detail, name="notification-detail"),
    path('notifications/unviewed/', notification_list, {'status': 'Непрочитано'}, name='notification-unviewed-list'),
    path('notifications/viewed/', notification_list, {'status': 'Прочитано'}, name='notification-viewed-list'),
]

