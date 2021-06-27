from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer)

from datetime import timedelta
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

from django.contrib.auth import authenticate
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _

from rest_framework.exceptions import PermissionDenied
from rest_framework import serializers

from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer,
    TokenRefreshSerializer,
    PasswordField
)
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.utils import UserType


class TokenPairSerializer(TokenObtainSerializer):
    default_error_messages = {
        'login_error': _('Username or Password does not matched .')
    }

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    @classmethod
    def get_user_type(cls, user):
        if user.is_superuser:
            return 'super_user'
        elif user.is_student:
            return 'student_user'
        elif user.is_teacher:
            return 'teacher_user'

    def validate(self, attrs):
        data = super().validate(attrs)
        self.validate_user()
        refresh = self.get_token(self.user)

        data['refresh_token'] = str(refresh)
        data['token'] = str(refresh.access_token)
        data['user_type'] = self.get_user_type(self.user)
        self.user.last_login = datetime.now()
        self.user.save()
        return data

    def validate_user(self):
        pass


class TeacherLoginSerializer(TokenPairSerializer):
    def validate_user(self):
        if self.user.user_type != UserType.teacher_user:
            raise serializers.ValidationError(
                _('User is not a teacher try again.'),
            )
        if not self.user.is_verified:
            raise AuthenticationFailed(_('User is not verified'), code='user_not_verified')


class StudentLoginSerializer(TokenPairSerializer):
    def validate_user(self):
        if self.user.user_type != UserType.student_user:
            raise serializers.ValidationError(
                _('User is not a student.'),
            )
        if not self.user.is_verified:
            raise AuthenticationFailed(_('User is not verified'), code='user_not_verified')

# class StaffLoginSerializer(TokenPairSerializer):
#     def validate_user(self):
#         if not self.user.is_staff:
#             raise serializers.ValidationError(
#                 _('Username or Password does not matched .'),
#             )
