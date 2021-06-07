import pytest
import json
from django.urls import reverse
from django.contrib.auth.models import User

from core.models import AnswerQuiz, Question, Quiz, Answer, AnswerChoice
from core.serializers import QuizSerializer, AnswerQuizSerializer, QuestionDTOSerializer
from quiz.dto import AnswerDTO, AnswersDTO, ChoiceDTO, QuestionDTO, QuizDTO

from .conftest import fixture_api_client, fixture_test_user, fixture_quiz_id_2


@pytest.fixture(name="list_quizzes")
def fixture_list_quizzes(django_db_setup, django_db_blocker):  # pylint: disable=unused-argument
    with django_db_blocker.unblock():
        user = User.objects.get(username="test_user")
        Quiz.create(QuizDTO("1", "Animals1", []))
        quiz2 = Quiz.create(QuizDTO("2", "Animals2_Start_Finish", []))
        user_quiz2 = AnswerQuiz.start_quiz(user, quiz2.uuid)
        user_quiz2.finished = True
        user_quiz2.save()
        quiz3 = Quiz.create(QuizDTO("3", "Animals3_Start", []))
        AnswerQuiz.start_quiz(user, quiz3.uuid)


@pytest.mark.django_db
def test_all_quiz(list_quizzes, api_client, test_user):  # pylint: disable=unused-argument
    response = api_client.get(reverse("core:quizzes_list", current_app="core"))
    quizzes = Quiz.objects.all()
    serializer = QuizSerializer(quizzes, many=True)
    print(response.data)
    assert response.data == serializer.data
    assert response.status_code == 200
    api_client.login(username="test_user", password="123")
    response = api_client.get(reverse("core:quizzes_list", current_app="core"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_started_quiz(list_quizzes, api_client, test_user):  # pylint: disable=unused-argument
    api_client.login(username="test_user", password="123")
    response = api_client.get(reverse("core:quizzes_list_started", current_app="core"))
    user = User.objects.get(username="test_user")
    quizzes = Quiz.objects.filter(answers_quiz__user=user)
    serializer = QuizSerializer(quizzes, many=True)
    print(response.data)
    assert response.data == serializer.data
    assert response.status_code == 200


@pytest.mark.django_db
def test_finished_quiz(list_quizzes, api_client, test_user):  # pylint: disable=unused-argument
    api_client.login(username="test_user", password="123")
    response = api_client.get(reverse("core:quizzes_list_finished", current_app="core"))
    user = User.objects.get(username="test_user")
    quizzes = Quiz.objects.filter(answers_quiz__user=user).filter(answers_quiz__finished=True)
    serializer = QuizSerializer(quizzes, many=True)
    print(response.data)
    assert response.data == serializer.data
    assert response.status_code == 200


@pytest.mark.django_db
def test_start_quiz(list_quizzes, api_client, test_user):  # pylint: disable=unused-argument
    api_client.login(username="test_user", password="123")
    response = api_client.post(
        reverse("core:quizzes_list_started", current_app="core"),
        data=json.dumps({"uuid": 1}),
        content_type="application/json",
    )
    answer = AnswerQuiz.objects.get(quiz__uuid=1)
    serializer = AnswerQuizSerializer(answer)
    print(response.data)
    assert response.data == serializer.data
    assert response.status_code == 201
    response = api_client.post(
        reverse("core:quizzes_list_started", current_app="core"),
        data=json.dumps({"uuid": "bad_id"}),
        content_type="application/json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_unauthorized(api_client):
    response = api_client.get(reverse("core:quizzes_list_started", current_app="core"))
    assert response.status_code == 403
    response = api_client.get(reverse("core:quizzes_list_finished", current_app="core"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_question(quizzes_full, api_client, test_user):
    api_client.login(username="test_user", password="123")
    quiz = Quiz.objects.get(uuid=2)
    response = api_client.get(reverse("core:questions", current_app="core", args=[quiz.slug]))
    serializer = QuestionDTOSerializer(quiz.questions.first().astuple())
    print(response.data)
    assert response.data == serializer.data
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_answer(quizzes_full, post_answer, api_client, test_user):
    api_client.login(username="test_user", password="123")
    quiz = Quiz.objects.get(uuid=2)
    response = api_client.post(
        reverse("core:questions", current_app="core", args=[quiz.slug]),
        data=json.dumps(post_answer),
        content_type="application/json",
    )
    print(response.data)
    assert response.status_code == 201
    answer_quiz = AnswerQuiz.objects.get(user__username="test_user")
    res = AnswerChoice.objects.select_related().filter(answer__answer_quiz=answer_quiz).first()
    assert res.answer.question_uuid == "2-1"
    assert res.text == "2-1-1"
    # print(answer_quiz.quiz.questions.answered(answer_quiz.questions_uuid).first().astuple())
    response = api_client.get(reverse("core:questions", current_app="core", args=[quiz.slug]))
    assert response.status_code == 200
    assert response.data["uuid"] == "2-2"
    # print(response.data)
    post_answer["choices"][0] = "2-1-2"
    response = api_client.patch(
        reverse("core:questions_prev", current_app="core", args=[quiz.slug]),
        data=json.dumps(post_answer),
        content_type="application/json",
    )
    assert response.status_code == 204
    print(response.data)
    answer_quiz = AnswerQuiz.objects.get(user__username="test_user")
    res = AnswerChoice.objects.select_related().filter(answer__answer_quiz=answer_quiz).first()
    assert res.answer.question_uuid == "2-1"
    assert res.text == "2-1-2"


@pytest.mark.django_db
@pytest.fixture(name="quizzes_empty")
def fixture_quizzes_full(django_db_setup, django_db_blocker):  # pylint: disable=unused-argument
    with django_db_blocker.unblock():
        user = User.objects.get(username="test_user")
        quiz = Quiz.create(QuizDTO("3", "Tест3", None))
        AnswerQuiz.start_quiz(user=user, uuid_quiz=quiz.uuid)


@pytest.mark.django_db
def test_empty_question(quizzes_empty, api_client, test_user):
    api_client.login(username="test_user", password="123")
    quiz = Quiz.objects.get(uuid=3)
    response = api_client.get(reverse("core:questions", current_app="core", args=[quiz.slug]))
    assert response.data == {"status": "the questions are over"}
    print(response.data)
    assert response.status_code == 404
