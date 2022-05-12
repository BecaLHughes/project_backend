# Django
from dataclasses import field
from rest_framework import serializers

# Local
from .models import Survey, SurveyQuestion, Score

# -------------------
class SurveyQuestionSerializer(serializers.ModelSerializer):
    question = serializers.CharField(source='question.text')
    options = serializers.SerializerMethodField()

    class Meta:
        model = SurveyQuestion
        fields = ['order', 'question', 'options']

    def get_options(self, _survey_question):
        return [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

class SurveySerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    
    class Meta: 
        model = Survey
        fields = ['id', 'title', 'questions']

    def get_questions(self, survey):
        survey_questions = SurveyQuestion.objects.filter(survey=survey)
        serializer = SurveyQuestionSerializer(survey_questions, many=True) 
        return serializer.data

class SurveyResponseSerializer(serializers.Serializer):
    question = serializers.IntegerField()
    value = serializers.IntegerField()

    def validate_question(self, question_id):
        survey = self.context["survey"]
        survey_question = SurveyQuestion.objects.filter(survey=survey, question__id=question_id).first()
        if survey_question is None:
            raise serializers.ValidationError({'question': f'Question with ID {question_id} does not exist for survey'})
        
        return question_id

    def validate_value(self, value):
        range = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        if (value in range) is False:
            raise serializers.ValidationError({'value': 'Must be a valid option'})
        
        return value

class ScoreSerialiser(serializers.ModelSerializer):
    score = serializers.IntegerField(source='value')
    feedback = serializers.CharField(source='feedback.text')

    class Meta: 
        model = Score
        fields = ['score', 'feedback', 'submitted']