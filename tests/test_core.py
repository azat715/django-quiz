import pytest

from core.models import Quiz


@pytest.mark.django_db
def test_fixture_db(content):
    quiz = Quiz.objects.count()
    assert quiz == 1
