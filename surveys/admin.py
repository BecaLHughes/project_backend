import imp
# Django
from django.contrib import admin

# Local
from .models import Survey, SurveyQuestion, Question, Feedback, Score

# --------------------------
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', )

class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'survey', 'question')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', )

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'range_lower', 'range_upper')

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'submitted', 'value', 'survey', 'feedback', )

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(SurveyQuestion, SurveyQuestionAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Score, ScoreAdmin)