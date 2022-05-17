# Python
import math

# Django
from django.utils import timezone

# Rest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Local
from .models import Feedback, Survey, Score
from .serializers import SurveySerializer, SurveyResponseSerializer, ScoreSerialiser

#--------------------------
class SurveyDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, survey_id):
        # Checking if survery with id exits
        survey = Survey.objects.filter(id=survey_id).first()
        if survey is None:
            return Response({'message': f'Survey with id {survey_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Serialising survey data
        serialiser = SurveySerializer(survey)
        return Response(serialiser.data)

class SurveyResponseView(APIView):
    permission_classes = [IsAuthenticated]

    def _create_or_update_score(self, request, survey, feedback, value):
        today = timezone.now().date()
        score = Score.objects.filter(survey=survey, user=request.user, submitted=today).first()
        if score is None:
            # Create a new score instance
            score = Score(value=value, survey=survey, feedback=feedback, user=request.user)
            score.save()
        else: 
            # Update the score value and feedback
            score.value = value
            score.feedback = feedback
            score.save()
        return score

    def get(self, request, survey_id):
        # Checking if survery with id exits
        survey = Survey.objects.filter(id=survey_id).first()
        if survey is None:
            return Response({'message': f'Survey with id {survey_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Get all scores for user and survey, ordered by date
        scores = Score.objects.filter(survey=survey, user=request.user)
        scores = scores.order_by('submitted')
        serializer = ScoreSerialiser(scores, many=True)
        return Response(serializer.data)

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
        score = self._create_or_update_score(request, survey, feedback, score_integer)
        score_serializer = ScoreSerialiser(score)
        return Response(score_serializer.data)