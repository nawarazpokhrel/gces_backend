from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from gces_backend import settings

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicons/favicon.ico')))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

schema_view = get_schema_view(
   openapi.Info(
      title="Tripnp Hotel Resource API",
      default_version='v1',
      description="Tripnp Hotel Resource API",
   ),
)

# API URLS
urlpatterns += [
    # API Docs
    path(
        'api/docs/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='api-docs'
    ),

    # api urls
    path(
        'api/v1/',
        include('config.api_urls')
    ),
]