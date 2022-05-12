# Django
from django.urls import path

# Local
from .views import UserLoginView, UserLogoutView, UserSignupView, UserProfileView

# -------------
urlpatterns = [
    path('login/', UserLoginView.as_view()),
    path('logout/', UserLogoutView.as_view()),
    path('', UserSignupView.as_view()),
    path('profile/', UserProfileView.as_view())
]
