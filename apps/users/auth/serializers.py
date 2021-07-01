from rest_framework_simplejwt.exceptions import AuthenticationFailed

from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken


class CustomTokenObtainSerializer(TokenObtainSerializer):
    default_error_messages = {
        'no_active_account': _('The user name or password is incorrect')
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


class LoginSerializer(CustomTokenObtainSerializer):
    def validate_user(self):
        if not self.user.is_verified:
            raise AuthenticationFailed(_('User is not verified'), code='user_not_verified')


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        data = {'token': str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh_token'] = str(refresh)

        return data

