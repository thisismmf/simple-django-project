from rest_framework import serializers
from .models import User

class MobileSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)

class PasswordSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)

class CodeVerifySerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile', 'full_name', 'email']