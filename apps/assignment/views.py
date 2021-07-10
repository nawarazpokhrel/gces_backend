from django.shortcuts import render

# Create your views here.
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.assignment import usecases, serializers
from apps.assignment.mixins import AssignmentMixin
from apps.materials.mixins import MaterialMixin
from apps.notice.permissions import IsTeacher, IsLibrarian
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response


class AddAssignmentView(generics.CreateAPIView):
    """
    Use this to add material
    """
    serializer_class = serializers.AddAssignmentSerializers
    permission_classes = [IsAuthenticated & IsTeacher]

    def perform_create(self, serializer):
        return usecases.AddAssignmentUseCase(serializer=serializer, user=self.request.user).execute()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response('Assignment added successfully', status=status.HTTP_201_CREATED)

    parser_classes = (FormParser, MultiPartParser)


class ListAssignmentView(generics.ListAPIView):
    """
    Use this to list material
    """
    serializer_class = serializers.ListAssignmentSerializers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return usecases.ListAssignmentUseCase().execute()


class UpdateAssignmentView(generics.UpdateAPIView, AssignmentMixin):
    """
    Use this to update assignment

    """
    serializer_class = serializers.UpdateAssignmentSerializers
    permission_classes = [IsAuthenticated & IsTeacher]
    queryset = ''
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return self.get_assignment()

    def perform_update(self, serializer):
        return usecases.UpdateAssignmentUseCase(serializer=serializer, assignment=self.get_object()).execute()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response("Assignment Updated successfully.")


class DeleteAssignmentView(generics.DestroyAPIView, AssignmentMixin):
    """
    Use this to delete material
    """
    permission_classes = [IsAuthenticated & IsTeacher]
    queryset = ''

    def get_object(self):
        return self.get_assignment()

    def perform_destroy(self, instance):
        return usecases.DeleteAssignmentUseCase(assignment=self.get_object()).execute()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("Deleted assignment successfully")
