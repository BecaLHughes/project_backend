# Django
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

# -------------------
class LoginSerialiser(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class SignupSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def create(self, validated_data):
        password = make_password(validated_data['password'])
        validated_data['password'] = password
        return super().create(validated_data)