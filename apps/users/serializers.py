from django.contrib import auth
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from apps.users.models import TeacherUser, StudentUser

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CreateUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'fullname',
            'email',
            'password',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }


class TeacherUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherUser
        fields = '_all__'


class CreateTeacherUserSerializer(CreateUserSerializer):
    # faculty = serializers.CharField()
    # faculty_code = serializers.CharField()
    # is_full_time = serializers.BooleanField()
    # joined_date = serializers.DateField()

    class Meta(CreateUserSerializer.Meta):
        pass


class CreateStudentUserSerializer(CreateUserSerializer):
    # faculty = serializers.CharField()
    # faculty_code = serializers.CharField()
    # joined_date = serializers.DateField()
    # registration_number = serializers.CharField()
    # parents_name = serializers.CharField()

    class Meta(CreateUserSerializer.Meta):
        pass


class ProfileSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'fullname',
            'email',
            'registration_number',
            'batch',
            'faculty',
            'faculty_code',
            'role'
        )


class UserProfileSerializer(serializers.Serializer):
    user = ProfileSerializer()


var = {
    "name": "Roshan Adhikari",
    "email": "",
    "regNo": "503",
    "phoneNumber": "",
    "batch": "2016",
    "role": "student",
    "faculty": "se"
}
