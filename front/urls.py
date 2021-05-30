from django.urls import path

from front.views import QuizzesList

app_name = "front"

urlpatterns = [
    path("", QuizzesList.as_view(), name="get_quizzes_list"),
]
