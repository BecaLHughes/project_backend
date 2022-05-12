# Python
import math

# Django
from django.shortcuts import render

# Rest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Local
from .models import Feedback, Survey, Score
from .serializers import SurveySerializer, SurveyResponseSerializer, ScoreSerialiser

#--------------------------
class SurveyMixinView(APIView):

    def get_survey(self, survey_id):
        # Checking if survery with id exits
        survey = Survey.objects.filter(id=survey_id).first()
        if survey is None:
            return Response({'message': f'Survey with id {survey_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        return survey

class SurveyDetailView(SurveyMixinView):
    permission_classes = [IsAuthenticated]

    def get(self, request, survey_id):
        # Checking if survery with id exits
        survey = self.get_survey(survey_id)

        # Serialising survey data
        serialiser = SurveySerializer(survey)
        return Response(serialiser.data)

class SurveyResponseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, survey_id):
        # Checking if survery with id exits
        survey = Survey.objects.filter(id=survey_id).first()
        if survey is None:
            return Response({'message': f'Survey with id {survey_id} does not exit'}, status=status.HTTP_404_NOT_FOUND)
        return Response({})

    def post(self, request, survey_id):
        # Checking if survery with id exits
        survey = Survey.objects.filter(id=survey_id).first()
        if survey is None:
            return Response({'message': f'Survey with id {survey_id} does not exit'}, status=status.HTTP_404_NOT_FOUND)

        # Checking if response data is valid
        response_serializer = SurveyResponseSerializer(data=request.data, many=True, context={'survey': survey})
        if not response_serializer.is_valid():
            return Response(data=response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Validating questions are not duplicates
        data = response_serializer.validated_data
        question_ids = [response['question'] for response in data]
        unique_id_count = len(set(question_ids))
        if len(question_ids) != unique_id_count:
            return Response(data={"message": "Duplicate responses not allowed"}, status=status.HTTP_400_BAD_REQUEST)

        # Finding average of response values
        values = [response['value'] for response in data]
        sum_of_values = sum(values)
        score_decimal = sum_of_values / len(values)
        score_integer = int(math.ceil(score_decimal))

        # Get feedback for response average score
        feedback = Feedback.objects.filter(range_lower__lte=score_integer, range_upper__gte=score_integer).first()
        
        # Create a score
        score = Score(value=score_integer, survey=survey, feedback=feedback, user=request.user)
        score.save()
        score_serializer = ScoreSerialiser(score)

        return Response(score_serializer.data)