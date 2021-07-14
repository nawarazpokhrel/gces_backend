from django.shortcuts import render
from rest_framework import generics as rest_generics
# Create your views here.
from apps.core import generics
from apps.core.mixins import ResponseMixin
from apps.result import usecases, serializers
from apps.users.mixins import UserMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


class AddResultView(generics.CreateAPIView, UserMixin,ResponseMixin):
    permission_classes = (AllowAny,)
    serializer_class = serializers.AddResultSerializer
    response_serializer_class = serializers.ResponseSerializer

    def get_object(self):
        return self.get_user()

    def perform_create(self, serializer):
        return usecases.AddResultUseCase(
            serializer=serializer,
            user=self.get_object(),
        ).execute()


    def response(self, serializer, result, status_code):
        serializer = self.get_response_serializer(result)
        return Response("Created")


class ListResultView(rest_generics.ListAPIView, UserMixin):
    serializer_class = serializers.ListResultSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        return self.get_user()

    def get_queryset(self):
        return usecases.ListResultUseCase(
            user=self.get_user()
        ).execute()
