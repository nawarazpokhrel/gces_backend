from django.shortcuts import render

# Create your views here.
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.notice import usecases, serializers
from apps.notice.permissions import IsTeacher, IsLibrarian
from rest_framework.parsers import FormParser, MultiPartParser


class AddNoticeView(generics.CreateAPIView):
    serializer_class = serializers.AddNoticeSerializers
    permission_classes = [IsAuthenticated & (IsTeacher | IsLibrarian)]

    def perform_create(self, serializer):
        return usecases.AddNoticeUseCase(serializer=serializer, user=self.request.user).execute()

    parser_classes = (FormParser, MultiPartParser)


    # @swagger_auto_schema(responses={201: MessageResponseSerializer()})
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
    #
    # def response(self, serializer, result, status_code):
    #     return Response(
    #         {
    #             'message': _('Added bus company staff.')
    #         },
    #         status=status_code
    #     )


class ListNoticeView(generics.ListAPIView):
    serializer_class = serializers.ListNoticeSerializers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return usecases.ListNoticeUseCase().execute()
