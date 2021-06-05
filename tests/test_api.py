import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import force_authenticate

from core.models import AnswerQuiz, Question, QuestionChoice, Quiz
from core.serializers import QuizSerializer
from quiz.dto import AnswerDTO, AnswersDTO, ChoiceDTO, QuestionDTO, QuizDTO

from .conftest import api_client


@pytest.fixture(name="list_quizes")
def list_quizes(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user = User.objects.create_user("test_user", "lennon@thebeatles.com", "123")
        Quiz.create(QuizDTO("1", "Animals1", []))
        quiz2 = Quiz.create(QuizDTO("2", "Animals2_Start_Finish", []))
        quiz3 = Quiz.create(QuizDTO("3", "Animals3_Start", []))
        user_quiz2 = AnswerQuiz.start_quiz(user, quiz2.slug)
        user_quiz2.finished = True
        user_quiz2.save()
        AnswerQuiz.start_quiz(user, quiz3.slug)


@pytest.mark.django_db
def test_all_quiz(list_quizes, api_client):
    response = api_client.get(reverse("core:quizzes_list", current_app="core"))
    quizzes = Quiz.objects.all()
    serializer = QuizSerializer(quizzes, many=True)
    print(response.data)
    assert response.data == serializer.data
    assert response.status_code == 200


@pytest.mark.django_db
def test_started_quiz(list_quizes, api_client):
    api_client.login(username="test_user", password="123")
    response = api_client.get(reverse("core:quizzes_list_started", current_app="core"))
    user = User.objects.get(username="test_user")
    quizzes = Quiz.objects.filter(answers_quiz__user=user)
    serializer = QuizSerializer(quizzes, many=True)
    print(response.data)
    assert response.data == serializer.data
    assert response.status_code == 200


@pytest.mark.django_db
def test_finished_quiz(list_quizes, api_client):
    api_client.login(username="test_user", password="123")
    response = api_client.get(reverse("core:quizzes_list_finished", current_app="core"))
    user = User.objects.get(username="test_user")
    quizzes = Quiz.objects.filter(answers_quiz__user=user).filter(answers_quiz__finished=True)
    serializer = QuizSerializer(quizzes, many=True)
    print(response.data)
    assert response.data == serializer.data
    assert response.status_code == 200


@pytest.mark.django_db
def test_unauthorized(api_client):
    response = api_client.get(reverse("core:quizzes_list_started", current_app="core"))
    assert response.status_code == 403
    response = api_client.get(reverse("core:quizzes_list_finished", current_app="core"))
    assert response.status_code == 403
