from django.urls import path
from rest_framework_simplejwt.views import token_verify

from apps.users.auth import views

urlpatterns = [
    path(
        'teacher-login',
        views.TeacherLoginView.as_view(),
        name='teacher-login'
    ),
    path(
        'student-login',
        views.StudentLoginView.as_view(),
        name='student-login'
    )
]