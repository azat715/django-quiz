from django.conf import settings
from django.db import models
from django.utils.text import slugify

from quiz.dto import AnswerDTO, AnswersDTO, ChoiceDTO, QuestionDTO, QuizDTO


class Quiz(models.Model):
    """QuizDTO Database Model"""

    uuid = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    slug = models.SlugField(null=False, unique=True)

    @classmethod
    def create(cls, obj: QuizDTO):
        quiz = cls(uuid=obj.uuid, title=obj.title)
        quiz.save()
        return quiz

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Question(models.Model):
    """QuestionDTO Database Model"""

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    uuid = models.CharField(max_length=10)
    text = models.CharField(max_length=255)

    @classmethod
    def create(cls, obj: QuestionDTO, quiz):
        question = cls(uuid=obj.uuid, text=obj.text, quiz=quiz)
        question.save()
        return question


class QuestionChoice(models.Model):
    """ChoiceDTO Database Model"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    uuid = models.CharField(max_length=10)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField()

    @classmethod
    def create(cls, obj: ChoiceDTO, question):
        question_choice = cls(
            uuid=obj.uuid, text=obj.text, is_correct=obj.is_correct, question=question
        )
        question_choice.save()
        return question_choice


class AnswerQuiz(models.Model):
    """AnswersDTO Database Model"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="answers_quiz"
    )
    quiz_uuid = models.CharField(max_length=10)
    finished = models.BooleanField(default=False)


class Answer(models.Model):
    """AnswerDTO Database Model"""

    answer_quiz = models.ForeignKey(AnswerQuiz, on_delete=models.CASCADE, related_name="answers")
    question_uuid = models.CharField(max_length=10)


class AnswerChoice(models.Model):
    """AnswerDTO.choices Database Model"""

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=255)
