from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        exclude = ('confirmation_code',)


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)
