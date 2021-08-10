import uuid

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import RegisterSerializer, TokenSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['patch', 'get'])
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class SignupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['post'])
    def signup(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            confirmation_code = uuid.uuid4()
            User.objects.create(username=username,
                                email=email,
                                confirmation_code=confirmation_code)
            send_mail(
                'Подтверждение пользователя',
                f'Код верификации: {confirmation_code}',
                None,
                [email],
                fail_silently=False,
            )
            return Response({'email': email,
                             'username': username},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['post'])
    def token(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            confirmation_code = serializer.validated_data.get(
                'confirmation_code')
            user = get_object_or_404(User, username=username)
            try:
                user = User.objects.get(username=username,
                                        confirmation_code=confirmation_code)
            except User.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            refresh_token = RefreshToken.for_user(user)
            return Response({'token': str(refresh_token.access_token)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
