from django.contrib.auth import get_user_model

from rest_framework.exceptions import ValidationError
from apps.users.models import TeacherUser

User = get_user_model()


class CreateTeacherUserUseCase:
    def __init__(self, serializer):
        self._serializer = serializer
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        password = self._data.pop('password')
        teacher_details = {
            'faculty': self._data.pop('faculty'),
            'faculty_code': self._data.pop('faculty_code'),
            'is_full_time': self._data.pop('is_full_time'),
            'joined_date': self._data.pop('joined_date'),
        }
        user = User(**self._data, is_teacher=True)
        user.set_password(password)
        user.save()
        try:
            user_instance = User.objects.get(id=user.id)
        except User.DoesNotExist:
            raise ValidationError('User does not exists')
        teacher = TeacherUser(
            **teacher_details,
            user=user_instance
        )
        teacher.save()
