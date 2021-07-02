from apps.users.email import ConfirmationEmail
from apps.users.models import TeacherUser, StudentUser

from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework_simplejwt.tokens import RefreshToken
from gces_backend.tasks import send_email

User = get_user_model()


class BaseUserUseCase:
    pass


class CreateTeacherUserUseCase:
    def __init__(self, serializer, request):
        self._serializer = serializer
        self._data = serializer.validated_data
        self._request = request

    def execute(self):
        self._factory()
        self._send_email()

    def _factory(self):
        password = self._data.pop('password')
        # teacher_details = {
        #     'faculty': self._data.pop('faculty'),
        #     'faculty_code': self._data.pop('faculty_code'),
        #     'is_full_time': self._data.pop('is_full_time'),
        #     'joined_date': self._data.pop('joined_date'),
        # }
        self.user = User(**self._data, is_teacher=True)
        self.user.set_password(password)
        # try:
        #     self.user.clean()
        # except DjangoValidationError as e:
        #     raise ValidationError(e.message_dict)
        self.user.save()
        try:
            self.user_instance = User.objects.get(id=self.user.id)
        except User.DoesNotExist:
            raise ValidationError('User does not exist')

    def _send_email(self):
        token = RefreshToken.for_user(user=self.user_instance).access_token
        # get current site
        current_site = get_current_site(self._request).domain
        # we are calling verify by email view  here whose name path is activate-by-email
        relative_link = reverse('activate-by-email')
        # make whole url
        absolute_url = 'http://' + current_site + relative_link + "?token=" + str(token)
        self.context = {
            'user': self.user_instance.fullname,
            'token': absolute_url
        }
        receipent = self.user.email
        ConfirmationEmail(context=self.context).send(to=[receipent])
        # send_email.delay(receipent, **self.context)


class CreateStudentUserUseCase:
    def __init__(self, serializer, request):
        self._serializer = serializer
        self._data = serializer.validated_data
        self._request = request

    def execute(self):
        self._factory()
        self._send_email()

    def _factory(self):
        password = self._data.pop('password')
        # student_details = {
        #     'faculty': self._data.pop('faculty'),
        #     'faculty_code': self._data.pop('faculty_code'),
        #     'joined_date': self._data.pop('joined_date'),
        #     'registration_number': self._data.pop('registration_number'),
        #     'parents_name': self._data.pop('parents_name')
        # }
        user = User(**self._data, is_student=True)
        user.set_password(password)
        try:
            user.clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)
        user.save()
        try:
            # Get user
            self.user_instance = User.objects.get(
                id=user.id,
            )
        except User.DoesNotExist:
            raise ValidationError('User does not exists')

    def _send_email(self):
        token = RefreshToken.for_user(user=self.user_instance).access_token
        # get current site
        current_site = get_current_site(self._request).domain
        # we are calling verify by email view  here whose name path is activate-by-email
        relative_link = reverse('activate-by-email')
        # make whole url
        absolute_url = 'http://' + current_site + relative_link + "?token=" + str(token)
        self.context = {
            'user': self.user_instance.fullname,
            'token': absolute_url
        }
        receipent = self.user_instance.email
        # ConfirmationEmail(context=self.context).send(to=[receipent])
        send_email.delay(receipent, **self.context)


class UserNotFound(NotFound):
    default_detail = _('User Not found.')


class GetUserUseCase:
    def __init__(self, user_id):
        self._user_id = user_id

    def execute(self):
        self._factory()
        return self.user

    def _factory(self):
        try:
            self.user = User.objects.get(pk=self._user_id)
        except User.DoesNotExist:
            raise UserNotFound


class UserProfileUseCase:
    def __init__(self, user):
        self._user_id = user

    def execute(self):
        self._factory()
        return self.user

    def _factory(self):
        try:
            self.user = User.objects.get(pk=self._user_id.id)
        except User.DoesNotExist:
            raise UserNotFound
