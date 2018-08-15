from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserSerializer, CreateUserSerializer
)


User = get_user_model()


class UserView(GenericAPIView):
    """
    Get user information
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response(self.get_serializer(request.user).data,
                        status=status.HTTP_200_OK)


class CreateUserView(GenericAPIView):
    """
    Registration user
    """
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data,
                        status=status.HTTP_201_CREATED)
