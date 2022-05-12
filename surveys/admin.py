import imp
# Django
from django.contrib import admin

# Local
from .models import Survey, Feedback, Question, Score

# --------------------------
class SurveyAdmin(admin.ModelAdmin):
    pass

class FeedbackAdmin(admin.ModelAdmin):
    pass

class QuestionAdmin(admin.ModelAdmin):
    pass

class ScoreAdmin(admin.ModelAdmin):
    pass

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Score, ScoreAdmin)