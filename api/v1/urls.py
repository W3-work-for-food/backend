from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (ContentViewSet, AmbassadorStatusView,
SentMerchViewSet, UserAPIView, MerchViewSet)


router = DefaultRouter()
router.register('content', ContentViewSet, basename='content')
router.register(
    'ambassador_status',
    AmbassadorStatusView,
    basename='ambassador_status'
)

router.register('merch', MerchViewSet, basename='merch')
router.register('sentmerch', SentMerchViewSet, basename='sentmerch')

urlpatterns = [
    path('getuser', UserAPIView.as_view()),
    path('', include(router.urls))
]
