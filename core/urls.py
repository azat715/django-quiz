from django.urls import path

from core.views import get_quizzes

app_name = "core"

urlpatterns = [
    path("quizzes/", get_quizzes, name="get_quizzes_list"),
]