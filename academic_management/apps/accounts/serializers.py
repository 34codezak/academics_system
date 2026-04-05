from rest_framework import serializers
from .models import User

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

