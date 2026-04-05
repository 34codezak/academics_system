from rest_framework import serializers
from .models import User
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    id = serializers(source='name', read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ['username',
                  'email', 
                  'phone', 
                  'password', 
                  'is_active', 
                  'created',
                  'updated'
        ]
        read_only_fields = ['username', 'email', 'is_active', 'created', 'updated']

class RegisterSerializer(UserSerializer):
    """Registration serializer for requests and user creation"""

    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)

    class Meta:
        model = User
        # List all the fields that can be included in a request or a response
        fields = [
            'username',
        'email',
        'password',
        ]

    def create(self, validated_data):
        return User.objects.create_user(**self.validated_data)

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data['accounts'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

