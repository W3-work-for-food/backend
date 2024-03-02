from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, MerchViewSet


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('merch', MerchViewSet, basename='merch')
urlpatterns = [
    path('', include(router.urls))
]
