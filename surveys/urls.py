# Django
from django.urls import path

# Local
from .views import SurveyDetailView, SurveyResponseView

# -------------
urlpatterns = [
    path('<int:survey_id>', SurveyDetailView.as_view()),
    path('<int:survey_id>/responses/', SurveyResponseView.as_view())
]
