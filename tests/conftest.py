from typing import List

import pytest
from core.models import (Answer, AnswerChoice, AnswerQuiz, Question,
                         QuestionChoice, Quiz)
from django.contrib.auth.models import User
from quiz.dto import AnswerDTO, AnswersDTO, ChoiceDTO, QuestionDTO, QuizDTO
from rest_framework.test import APIClient


@pytest.fixture(name="quiz_id_1")
def fixture_quiz_id_1():
    choices: List[ChoiceDTO] = [
        ChoiceDTO("1-1-1", "An elephant", True),
        ChoiceDTO("1-1-2", "A mouse", False),
    ]
    questions: List[QuestionDTO] = [QuestionDTO("1-1", "Who is bigger?", choices)]
    return QuizDTO("1", "Animals", questions)


@pytest.fixture(name="quiz_id_2")
def fixture_quiz_id_2():
    choices_1: List[ChoiceDTO] = [
        ChoiceDTO("2-1-1", "Вариант А", True),
        ChoiceDTO("2-1-2", "Вариант B", False),
        ChoiceDTO("2-1-3", "Вариант C", False),
        ChoiceDTO("2-1-4", "Вариант D", False),
    ]
    questions: List[QuestionDTO] = [QuestionDTO("2-1", "Вопрос 1", choices_1)]
    choices_2: List[ChoiceDTO] = [
        ChoiceDTO("2-2-1", "Вариант А", False),
        ChoiceDTO("2-2-2", "Вариант B", True),
        ChoiceDTO("2-2-3", "Вариант C", True),
        ChoiceDTO("2-2-4", "Вариант D", False),
    ]
    questions.append(QuestionDTO("2-2", "Вопрос 2", choices_2))
    choices_3: List[ChoiceDTO] = [
        ChoiceDTO("2-3-1", "Вариант А", False),
        ChoiceDTO("2-3-2", "Вариант B", False),
        ChoiceDTO("2-3-3", "Вариант C", False),
        ChoiceDTO("2-3-4", "Вариант D", True),
    ]
    questions.append(QuestionDTO("2-3", "Вопрос 3", choices_3))
    return QuizDTO("2", "Tест", questions)


@pytest.fixture(scope="session", name="api_client")
def fixture_api_client():
    return APIClient()


@pytest.mark.django_db
@pytest.fixture(scope="session", name="test_user")
def fixture_test_user(django_db_setup, django_db_blocker):  # pylint: disable=unused-argument
    with django_db_blocker.unblock():
        User.objects.create_user("test_user", "lennon@thebeatles.com", "123")


@pytest.mark.django_db
@pytest.fixture(name="quizzes_full")
def fixture_quizzes_full(
    django_db_setup, django_db_blocker, quiz_id_2
):  # pylint: disable=unused-argument
    with django_db_blocker.unblock():
        user = User.objects.get(username="test_user")
        quiz = Quiz.create(quiz_id_2)
        for question in quiz_id_2[2]:
            q = Question.create(question, quiz)
            for choice in question[2]:
                QuestionChoice.create(choice, q)
        AnswerQuiz.start_quiz(user=user, uuid_quiz=quiz.uuid)


@pytest.fixture(name="post_answer")
def fixture_post_answer():
    return {
        "question_uuid": "2-1",
        "choices": [
            "2-1-1",
        ],
    }


@pytest.fixture(name="answers_dto")
def fixture_quiz_answers_dto():
    answers: List[AnswerDTO] = [AnswerDTO("1-1", ["1-1-1"])]
    return AnswersDTO("1", answers)


@pytest.mark.django_db
@pytest.fixture(name="answers_dto_db")
def fixture_answers_dto_db(answers_dto):
    user = User.objects.get(username="test_user")
    quiz = Quiz.objects.first()
    answer = AnswerQuiz.start_quiz(user, quiz.uuid)
    for item in answers_dto.answers:
        a = Answer.create(item, answer)
        for choice in item.choices:
            AnswerChoice(answer=a, text=choice).save()


@pytest.mark.django_db
@pytest.fixture(name="quiz_id_1_db")
def fixture_quiz_id_1_db(django_db_setup, django_db_blocker, quiz_id_1):
    quiz = Quiz.create(quiz_id_1)
    for question in quiz_id_1[2]:
        q = Question.create(question, quiz)
        for choice in question[2]:
            QuestionChoice.create(choice, q)
