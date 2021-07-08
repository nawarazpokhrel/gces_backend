from django.shortcuts import render

# Create your views here.
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.notice import usecases, serializers
from apps.notice.permissions import IsTeacher, IsLibrarian
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response


class AddNoticeView(generics.CreateAPIView):
    serializer_class = serializers.AddNoticeSerializers
    permission_classes = [IsAuthenticated & (IsTeacher | IsLibrarian)]

    def perform_create(self, serializer):
        return usecases.AddNoticeUseCase(serializer=serializer, user=self.request.user).execute()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response('Notice created successfully', status=status.HTTP_201_CREATED)

    parser_classes = (FormParser, MultiPartParser)


class ListNoticeView(generics.ListAPIView):

    serializer_class = serializers.ListNoticeSerializers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return usecases.ListNoticeUseCase().execute()
