# Django
from urllib import response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Rest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Local
from .serializers import LoginSerialiser, SignupSerializer, UserProfileSerializer

# -----------------------
class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerialiser(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            return Response({'message': 'Username or password incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        Token.objects.get(user=request.user).delete()
        return Response()

class UserSignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update user details
        serializer.update(request.user, serializer.validated_data)
        return Response(serializer.data)

    def delete(self, request):
        # Delete user
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)