# Django
from django.shortcuts import render

# Rest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Local

#--------------------------
class Survey(APIView):
    def post(self, request):
        return Response()

class Feedback(APIView):
    def post(self, request):
        return Response()

        
