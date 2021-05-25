from django.contrib.auth.models import User
from django.db import models


class Quiz(models.Model):
    """QuizDTO"""

    uuid = models.CharField(max_length=10)
    title = models.CharField(max_length=50)


class Question(models.Model):
    """QuestionDTO"""

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    uuid = models.CharField(max_length=10)
    text = models.CharField(max_length=255)


class QuestionChoice(models.Model):
    """ChoiceDTO"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    uuid = models.CharField(max_length=10)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField()


class AnswerQuiz(models.Model):
    """AnswersDTO"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers_quiz")
    quiz_uuid = models.CharField(max_length=10)


class Answer(models.Model):
    """AnswerDTO"""

    answer_quiz = models.ForeignKey(AnswerQuiz, on_delete=models.CASCADE, related_name="answers")
    question_uuid = models.CharField(max_length=10)


class AnswerChoice(models.Model):
    """AnswerDTO.choices"""

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=255)
