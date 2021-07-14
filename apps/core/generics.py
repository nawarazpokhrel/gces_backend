from rest_framework import generics, status
from rest_framework.response import Response


class CreateAPIView(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.perform_create(serializer)
        return self.response(serializer=serializer, result=result, status_code=status.HTTP_201_CREATED)

    def response(self, serializer, result, status_code):
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status_code, headers=headers)
