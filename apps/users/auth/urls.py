from django.urls import path
from rest_framework_simplejwt.views import token_verify

from apps.users.auth import views

urlpatterns = [
    path(
        'login',
        views.LoginView.as_view(),
        name='login'
    ),
    path(
        'login-refresh',
        views.LoginRefreshView.as_view(),
        name='login-refresh'
    ),
]