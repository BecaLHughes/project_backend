# Django
from django.shortcuts import render

# Rest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Local
from .models import Survey
from .serializers import SurveySerializer, SurveyResponseSerializer

#--------------------------
class SurveyDetailView(APIView):
    def get(self, request, survey_id):
        survey = Survey.objects.filter(id=survey_id).first()
        if survey is None:
            return Response({'message': f'Survey with id {survey_id} does not exit'}, status=status.HTTP_404_NOT_FOUND)

        serialiser = SurveySerializer(survey)

        return Response(serialiser.data)

class SurveyResponseView(APIView):
    def post(self, request, survey_id):
        survey = Survey.objects.filter(id=survey_id).first()
        if survey is None:
            return Response({'message': f'Survey with id {survey_id} does not exit'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SurveyResponseSerializer(data=request.data, many=True, context={'survey': survey})
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        question_ids = [response['question'] for response in data]
        unique_id_count = len(set(question_ids))
        if len(question_ids) != unique_id_count:
            return Response(data={"message": "Duplicate responses not allowed"}, status=status.HTTP_400_BAD_REQUEST)

        values = [response['value'] for response in data]
        sum_of_values = sum(values)
        print(sum_of_values)

        return Response({})