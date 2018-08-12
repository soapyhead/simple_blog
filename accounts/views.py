from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserSerializer, LoginUserSerializer, CreateUserSerializer
)


User = get_user_model()


class UserView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response(self.get_serializer(request.user).data,
                        status=status.HTTP_200_OK)


class CreateUserView(GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data,
                        status=status.HTTP_201_CREATED)


class LoginUserView(GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'].lower()
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)

                if not created:
                    token.created = timezone.now()
                    token.save()

                data = serializer.validated_data
                data['key'] = token.key
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'authentication failed'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class LogoutUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)