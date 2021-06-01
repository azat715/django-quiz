from typing import List

from django.contrib.auth.models import User

import pytest
from core.models import Quiz, Question, QuestionChoice
from quiz.dto import AnswerDTO, AnswersDTO, ChoiceDTO, QuestionDTO, QuizDTO


@pytest.fixture()
def question():
    choices: List[ChoiceDTO] = [
        ChoiceDTO("1-1-1", "An elephant", True),
        ChoiceDTO("1-1-2", "A mouse", False),
    ]
    return QuestionDTO("1-1", "Who is bigger?", choices)


@pytest.fixture(scope="session")
def content(django_db_setup, django_db_blocker):
    choices: List[ChoiceDTO] = [
        ChoiceDTO("1-1-1", "An elephant", True),
        ChoiceDTO("1-1-2", "A mouse", False),
    ]
    questions: List[QuestionDTO] = [QuestionDTO("1-1", "Who is bigger?", choices)]
    quiz: QuizDTO = QuizDTO("1", "Animals", questions)
    with django_db_blocker.unblock():
        quiz_db = Quiz.create(quiz)
        question_db = Question.create(questions[0], quiz_db)
        QuestionChoice.create(choices[0], question_db)
        QuestionChoice.create(choices[1], question_db)
        User.objects.create_user("test_user", "lennon@thebeatles.com", "123")
