from django.urls import path

from core.views import (
    quizzes,
    quizzes_started,
    quizzes_finished,
    questions,
    questions_prev,
    quiz_score,
)

app_name = "core"

urlpatterns = [
    path("quizzes/", quizzes, name="quizzes_list"),
    path("quizzes/started", quizzes_started, name="quizzes_list_started"),
    path("quizzes/finished", quizzes_finished, name="quizzes_list_finished"),
    path("quizzes/<slug:slug>/question", questions, name="questions"),
    path("quizzes/<slug:slug>/question/prev", questions_prev, name="questions_prev"),
    path("quizzes/<str:slug>/score", quiz_score, name="quiz_score"),
]
