from collections import OrderedDict

import pytest
from core.models import AnswerQuiz, Quiz
from core.serializers import AnswerPOSTSerializer, QuestionDTOSerializer
from quiz.dto import AnswerDTO


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
    serializer = AnswerPOSTSerializer(data=post_answer)
    if serializer.is_valid():
        answer = serializer.save()
        assert answer == AnswerDTO(question_uuid="2-1", choices=["2-1-1"])
        print(answer)
    print(serializer.errors)
    assert serializer.errors == {}


@pytest.mark.django_db
def test_answer_quiz(quizzes_full, quiz_id_2, test_user):
    answers = AnswerQuiz.objects.first()
    question = answers.get_question()
    print(question)
    assert question == quiz_id_2[2][0]


@pytest.mark.django_db
def test_serialize_quiz(quiz_id_1_db, quiz_id_1):
    quiz = Quiz.objects.first()
    quiz_dto = quiz.astuple()
    print(quiz_dto)
    assert quiz_dto == quiz_id_1


@pytest.mark.django_db
def test_serialize_answers(test_user, quiz_id_1_db, answers_dto_db, answers_dto):
    answer = AnswerQuiz.objects.first()
    answer_dto_test = answer.astuple()
    print(answer_dto_test)
    assert answer_dto_test == answers_dto


@pytest.mark.django_db
def test_get_score(quiz_id_1_db, answers_dto_db, answers_dto, test_user):
    answer_quiz = AnswerQuiz.objects.first()
    score = answer_quiz.get_score()
    print(score)
    assert score == 1.0
    answers_dto.answers[0].choices[0] = "1-1-2"
    answer_quiz.update_prev_answer(answers_dto.answers[0])
    score = answer_quiz.get_score()
    print(score)
    assert score == 0
