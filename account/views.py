from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from account.models import User, UserResetPassword

from account.serializers import LoginSerializer, UserSerializer, RegisterUserSerializer, \
    SendResetPasswordKeySerializer, ResetPasswordSerializer
from account.services import ResetPasswordManager


class LoginGenericAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        if user:
            token = Token.objects.get_or_create(user=user)[0]
            user_serializer = UserSerializer(instance=user, context={'request': request})
            return Response({
                **user_serializer.data,
                'token': token.key,
            })
        return Response({'message': 'The user is not found or the password is invalid'},
                        status=status.HTTP_400_BAD_REQUEST)


class RegisterGenericAPIView(GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get_or_create(user=user)[0]
        user_serializer = UserSerializer(instance=user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key,
        })


class SendResetPasswordKeyApiView(GenericAPIView):

    serializer_class = SendResetPasswordKeySerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email', None)
        user = get_object_or_404(User, email=email)
        manager = ResetPasswordManager(user)
        manager.send_key()
        return Response({'detail': 'Ключ успещно отправлен'})


class ResetPasswordApiView(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        key = serializer.validated_data.get('key', None)
        new_password = serializer.validated_data.get('new_password', None)
        user = get_object_or_404(UserResetPassword, key=key).user
        manager = ResetPasswordManager(user)
        is_changed = manager.reset_password(key, new_password)
        return Response(
            {'is_changed': is_changed},
            status=status.HTTP_200_OK if is_changed else status.HTTP_400_BAD_REQUEST
        )