# Django
from django.urls import path

# Local
from .views import Survey, Feedback

# -------------
urlpatterns = [
    path('surveys/', Survey.as_view()),
    path('feedback/', Feedback.as_view())
]
