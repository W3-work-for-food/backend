from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (AmbassadorsViewSet, ContentViewSet, MerchViewSet,
                          SentMerchViewSet, UserAPIView, notification_detail,
                          notification_list)
from api.v1.ya_form_views import ambassadors_form_get

router_v1 = DefaultRouter()
router_v1.register('merch', MerchViewSet, basename='merch')
router_v1.register('ambassadors', AmbassadorsViewSet, basename='ambassadors')
router_v1.register(
    r'ambassadors/(?P<ambassador_id>\d+)/content',
    ContentViewSet, basename='content'
)
router_v1.register(
    r'ambassadors/(?P<ambassador_id>\d+)/sentmerch',
    SentMerchViewSet, basename='sentmerch'
)

urlpatterns = [
    path('getuser/', UserAPIView.as_view()),
    path('', include(router_v1.urls)),
    path(
        'notifications/<int:pk>/',
        notification_detail,
        name="notification-detail"
    ),
    path(
        'notifications/unviewed/',
        notification_list,
        {'status': 'unread'},
        name='notification-unviewed-list'
    ),
    path(
        'notifications/viewed/',
        notification_list,
        {'status': 'read'},
        name='notification-viewed-list'
    ),
    path(
        'ambassadorsform/',
        ambassadors_form_get,
        name='ambassadors-form-get'
    ),
]
