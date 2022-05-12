# Django
from django.db import models
from django.contrib.auth.models import User

# ------------
class Survey(models.Model):
    title = models.CharField(max_length=100)
    questions = models.ManyToManyField('Question', through='SurveyQuestion')

    def __str__(self) -> str:
        return self.title

class SurveyQuestion(models.Model):
    # Fields
    order = models.PositiveIntegerField()

    # Relations
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

class Question(models.Model):
    text = models.TextField()

    def __str__(self) -> str:
        return self.text

class Feedback(models.Model):
    text = models.TextField()
    range_upper = models.IntegerField()
    range_lower = models.IntegerField()

    def __str__(self) -> str:
        return self.text

class Score(models.Model):
    # Fields
    value = models.IntegerField()
    submitted = models.DateField(auto_now_add=True)

    # Relations
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
