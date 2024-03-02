from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ContentView, AmbassadorStatusView


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('content', ContentView, basename='content')
router.register(
    'ambassador_status',
    AmbassadorStatusView,
    basename='ambassador_status'
)
urlpatterns = [
    path('', include(router.urls))
]
