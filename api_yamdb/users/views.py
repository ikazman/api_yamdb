import uuid

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


class SignupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['post'])
    def signup(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
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
            return Response({'status': 'Код верификации отправлен'},
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class TokenViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['post'])
    def token(self, request):
        serializer = TokenSerializer(data=self.request.data)
        serializer.is_valid()
        username = serializer.data['username']
        confirmation_code = serializer.data['confirmation_code']
        user = User.objects.get(username=username,
                                confirmation_code=confirmation_code)
        refresh_token = RefreshToken.for_user(user)
        return Response({'token': str(refresh_token.access_token)})
