from django.shortcuts import render
import jwt
from django.contrib.auth import get_user_model

# Create your views here.
from apps.users import usecases, serializers
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny

from apps.users.mixins import UserMixin
from gces_backend.settings import SECRET_KEY

User = get_user_model()


class CreateTeacherUserView(generics.CreateAPIView):
    serializer_class = serializers.CreateTeacherUserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        return usecases.CreateTeacherUserUseCase(serializer=serializer, request=self.request).execute()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response('Teacher user created successfully', status=status.HTTP_201_CREATED)


class CreateStudentUserView(generics.CreateAPIView):
    serializer_class = serializers.CreateStudentUserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        return usecases.CreateStudentUserUseCase(serializer=serializer, request=self.request).execute()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response('Student created successfully', status=status.HTTP_201_CREATED)


class VerifyEmailAndSubscribeEmailView(generics.GenericAPIView):
    """
    Use this to verify user email
    """
    serializer_class = None
    permission_classes = (AllowAny,)

    def get(self, request):
        # First get token from user browser
        token = request.GET.get('token')
        try:
            # decoding the token along with secret key
            payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
            # get the user that sent the payload
            user = User.objects.get(id=payload['user_id'])
            # now verify the user
            user.is_verified = True
            user.save()
            return Response('Successfully verified', status=status.HTTP_200_OK)
        # raise exceptions if token expired
        except jwt.ExpiredSignatureError as e:
            return Response({'error': 'Activations link expired'}, status=status.HTTP_400_BAD_REQUEST)
        # raise exception if the token sent is wrong
        except jwt.exceptions.DecodeError as e:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView,UserMixin):
    serializer_class = serializers.UserProfileSerializer

    def get_object(self):
        return self.get_user()

