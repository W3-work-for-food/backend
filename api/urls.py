"""URL-роутинг приложения API."""
from django.urls import include, path

from mvp_crm.urls import VERSION_API

urlpatterns = [
    path(f'v{VERSION_API}/', include(f'api.v{VERSION_API}.urls')),
]
