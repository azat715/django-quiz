from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from front.views import QuizzesList

app_name = "front"

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", QuizzesList.as_view(), name="get_quizzes_list"),
]
