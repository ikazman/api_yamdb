from rest_framework import serializers


from .models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('bio',
                  'email',
                  'first_name',
                  'last_name',
                  'role',
                  'username')


class RegisterSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('"me" not allowed as username')
        return value

    def validate_unique(self, data):
        email = self.context.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('"me" not allowed as username')
        return data

    class Meta:
        model = User
        fields = ('username', 'email',)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)
