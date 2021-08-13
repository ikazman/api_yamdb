from collections import UserList
import uuid

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrStaff
from .models import User
from .serializers import RegisterSerializer, TokenSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]

    @action(detail=False,
            permission_classes=[IsAuthenticated],
            methods=['PATCH', 'GET'])
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        
        if request.method == 'PATCH':
            serializer = self.get_serializer(user,
                                             data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SignupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['POST'])
    def signup(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username, email=email)
            self.sent_code(user, email)
            return Response({'email': email,
                             'username': username},
                            status=status.HTTP_200_OK)
        user = User.objects.create(username=username,
                                   email=email)
        self.sent_code(user, email)
        return Response({'email': email,
                         'username': username},
                        status=status.HTTP_200_OK)

    def sent_code(self, user, email):
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Подтверждение пользователя',
            f'Код верификации: {confirmation_code}',
            None,
            [email],
            fail_silently=False,
        )


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
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if default_token_generator.check_token(user, confirmation_code):
                refresh_token = RefreshToken.for_user(user)
                return Response({'token': str(refresh_token.access_token)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
