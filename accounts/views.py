# Django
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Rest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Local
from .serializers import LoginSerialiser, SignupSerializer

# -----------------------
class UserLogin(APIView):
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

class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        Token.objects.get(user=request.user).delete()
        return Response()

class UserSignup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})