from collections import OrderedDict
import pytest

from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer


from core.serializers import QuestionDTOSerializer, AnswerSerializer
from core.models import Quiz, AnswerQuiz, QuestionChoice
from quiz.services import AnswerDTO


@pytest.fixture(name="question_json")
def fixture_question_json():
    return {
        "uuid": "1-1",
        "text": "Who is bigger?",
        "choices": [
            OrderedDict([("uuid", "1-1-1"), ("text", "An elephant")]),
            OrderedDict([("uuid", "1-1-2"), ("text", "A mouse")]),
        ],
    }


def test_q_DTOSerializer(quiz_id_1, question_json):
    serializer = QuestionDTOSerializer(quiz_id_1.questions[0])
    print(serializer.data)
    assert serializer.data == question_json


def test_answer_serialize(post_answer):
    serializer = AnswerSerializer(data=post_answer)
    if serializer.is_valid():
        answer = serializer.save()
        assert answer == AnswerDTO(question_uuid="2-1", choices=["2-1-1"])
        print(answer)
    print(serializer.errors)


@pytest.mark.django_db
def test_answer_quiz(quizzes_full, quiz_id_2, test_user):
    """почему то fixture fixture_test_user срабатывает если тесты запускать все"""
    answers = AnswerQuiz.objects.first()
    question = answers.get_question()
    print(question)
    assert question == quiz_id_2[2][0]
