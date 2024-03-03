from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, ContentView, AmbassadorStatusView, GetUserViewSet, MerchViewSet


router = DefaultRouter()
router.register('content', ContentView, basename='content')
router.register(
    'ambassador_status',
    AmbassadorStatusView,
    basename='ambassador_status'
)

router.register('getusers', GetUserViewSet, basename='getusers')
router.register('merch', MerchViewSet, basename='merch')

urlpatterns = [
    path('', include(router.urls))
]
