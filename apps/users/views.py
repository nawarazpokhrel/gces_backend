from django.shortcuts import render

# Create your views here.
from apps.users import usecases, serializers
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.permissions import AllowAny


class CreateTeacherUserView(generics.CreateAPIView):
    serializer_class = serializers.CreateTeacherUserSerializer
    # authentication_classes = (AllowAny,)

    def perform_create(self, serializer):
        return usecases.CreateTeacherUserUseCase(serializer=serializer).execute()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response('created successfully', status=status.HTTP_201_CREATED)
