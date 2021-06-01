import pytest

from django.contrib.auth.models import User

from core.models import Quiz, AnswerQuiz


@pytest.mark.django_db
def test_fixture_db(content):
    quiz = Quiz.objects.count()
    assert quiz == 1


@pytest.mark.django_db
def test_quiz(content, question):
    user = User.objects.first()
    quiz = Quiz.objects.first()
    answers = AnswerQuiz.start_quiz(user, quiz.slug)
    assert answers.get_question() == question
