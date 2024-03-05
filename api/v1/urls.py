from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GetUserViewSet, AmbassadorsViewSet, MerchViewSet

router_v1 = DefaultRouter()
router_v1.register('getusers', GetUserViewSet, basename='getusers')
router_v1.register('merch', MerchViewSet, basename='merch')
router_v1.register('ambassadors', AmbassadorsViewSet, basename='ambassadors')
urlpatterns = [
    path('', include(router_v1.urls))
]
