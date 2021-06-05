from django.urls import path

from core.views import get_quizzes, get_quizzes_started, get_quizzes_finished

app_name = "core"

urlpatterns = [
    path("quizzes/", get_quizzes, name="quizzes_list"),
    path("quizzes/started", get_quizzes_started, name="quizzes_list_started"),
    path("quizzes/finished", get_quizzes_finished, name="quizzes_list_finished"),
]
