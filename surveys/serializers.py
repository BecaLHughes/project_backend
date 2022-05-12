# Django
from rest_framework import serializers

# -------------------
class SurveySerializer(serializers.Serializer):
    title = serializers.CharField()

class SurveyQuestionSerializer(serializers.Serializer):
    survey = serializers.CharField()
    question = serializers.CharField()
    order = serializers.IntegerField()

class QuestionSerializer(serializers.Serializer):
    text = serializers.CharField()

class FeedbackSerializer(serializers.Serializer):
    text = serializers.CharField()
    score_range = serializers.IntegerField()

class ScoreSerializer(serializers.Serializer):
    time_stamp = serializers.DateTimeField()
    score = serializers.IntegerField()
    feedback = serializers.CharField()

    

