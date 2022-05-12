# Django
from django.urls import path

# Local
from .views import UserLogin, UserLogout, UserSignup

# -------------
urlpatterns = [
    path('login/', UserLogin.as_view()),
    path('logout/', UserLogout.as_view()),
    path('signup/', UserSignup.as_view())
]
