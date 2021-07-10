"""gces_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



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




title = "Tripnp Hotel Resource API",
default_version = 'v1',
description = "Tripnp Hotel Resource API",
schema_view = get_schema_view(
    openapi.Info(
        title="GCES Backend",
        default_version='v1',
        description="GCES Backend API",
        contact=openapi.Contact(email="contact@snippets.local"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicons/favicon.ico')))
]
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

schema_view = get_schema_view(
    openapi.Info(
        title="GCES Backend",
        default_version='v1',
        description="GCES Backend API",
        contact=openapi.Contact(email="contact@snippets.local"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
                  path(
                      'admin/',
                      admin.site.urls
                  ),

                  path(
                      'api/v1/user/',
                      include('apps.users.urls')
                  ),
                  path(
                      'api/v1/notice/',
                      include('apps.notice.urls')
                  ),
                  path(
                      'api/v1/material/',
                      include('apps.materials.urls')
                  ),
                  path(
                      'api/v1/assignment/',
                      include('apps.assignment.urls')
                  ),

                  path(
                      'api/v1/user/auth/',
                      include('apps.users.auth.urls')
                  ),

                  path(
                      'api/docs/',
                      schema_view.with_ui('swagger', cache_timeout=0),
                      name='api-docs'
                  ),

                  path(
                      'redoc/',
                      schema_view.with_ui('redoc', cache_timeout=0),
                      name='schema-redoc'
                  ),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
