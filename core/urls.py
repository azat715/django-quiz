from django.urls import path

from core.views import get_quizzes, start_quiz

app_name = "core"

urlpatterns = [
    path("quizzes/", get_quizzes, name="get_quizzes_list"),
    path("quizzes/started", start_quiz, name="start_quiz"),
]
