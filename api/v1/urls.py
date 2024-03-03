from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GetUserViewSet, MerchViewSet


router = DefaultRouter()
router.register('getusers', GetUserViewSet, basename='getusers')
router.register('merch', MerchViewSet, basename='merch')
urlpatterns = [
    path('', include(router.urls))
]
