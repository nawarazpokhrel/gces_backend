from django.urls import path
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users import views

urlpatterns = [
    path(
        'register/teacher',
        views.CreateTeacherUserView.as_view(),
        name='Add-teacher-detail'
    ),
    path(
        'activate-by-email',
        views.VerifyEmailAndSubscribeEmailView.as_view(),
        name='activate-by-email'
    ),
]
