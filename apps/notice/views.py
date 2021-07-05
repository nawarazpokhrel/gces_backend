from django.shortcuts import render

# Create your views here.
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.notice import usecases, serializers
from apps.notice.permissions import IsTeacher, IsLibrarian


class AddNoticeView(generics.CreateAPIView):
    serializer_class = serializers.AddNoticeSerializers
    permission_classes = [IsAuthenticated & (IsTeacher | IsLibrarian)]

    def perform_create(self, serializer):
        return usecases.AddNoticeUseCase(serializer=serializer, user=self.request.user).execute()


class ListNoticeView(generics.ListAPIView):
    serializer_class = serializers.ListNoticeSerializers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return usecases.ListNoticeUseCase().execute()
