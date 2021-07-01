from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.auth import serializers


class LoginView(TokenObtainPairView):
    """
    Use this end-point to get access token for normal user
    """
    # logging_methods = ['POST']
    # throttle_scope = 'login'

    serializer_class = serializers.LoginSerializer

    # @swagger_auto_schema(responses={200: serializers.TokenPairSerializer()})
    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #
    #     try:
    #         serializer.is_valid(raise_exception=True)
    #     except TokenError as e:
    #         raise InvalidToken(e.args[0])
    #
    #     return Response(serializer.validated_data, status=status.HTTP_200_OK)

