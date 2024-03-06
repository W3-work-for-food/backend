from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (GetUserViewSet, AmbassadorsViewSet, MerchViewSet, \
    ContentViewSet, AmbassadorStatusView)

router_v1 = DefaultRouter()
router_v1.register('getusers', GetUserViewSet, basename='getusers')
router_v1.register('merch', MerchViewSet, basename='merch')
router_v1.register('ambassadors', AmbassadorsViewSet, basename='ambassadors')
router_v1.register('content', ContentViewSet, basename='content')
router_v1.register(
    'ambassador_status',
    AmbassadorStatusView,
    basename='ambassador_status'
)

urlpatterns = [
    path('', include(router_v1.urls))
]
