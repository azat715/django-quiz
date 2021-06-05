from django.conf import settings
from django.db import models
from django.utils.text import slugify

from quiz.dto import AnswerDTO, ChoiceDTO, QuestionDTO, QuizDTO


class Quiz(models.Model):
    """QuizDTO Database Model"""

    uuid = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    slug = models.SlugField(null=False, unique=True)

    def __repr__(self):
        return "Quiz({self.uuid}, {self.title}, {self.slug})".format(self=self)

    def __str__(self):
        return self.__repr__()

    @classmethod
    def create(cls, obj: QuizDTO):
        quiz = cls(uuid=obj.uuid, title=obj.title)
        quiz.save()
        return quiz

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class QuestionManager(models.Manager):
    def unanswered(self, uuids):
        return super().get_queryset().exclude(uuid__in=uuids)

    def answered(self, uuids):
        return super().get_queryset().filter(uuid__in=uuids)


class Question(models.Model):
    """QuestionDTO Database Model"""

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    uuid = models.CharField(max_length=10)
    text = models.CharField(max_length=255)

    objects = QuestionManager()

    def __repr__(self):
        return "Question({self.uuid}, {self.text})".format(self=self)

    def __str__(self):
        return self.__repr__()

    @classmethod
    def create(cls, obj: QuestionDTO, quiz):
        question = cls(uuid=obj.uuid, text=obj.text, quiz=quiz)
        question.save()
        return question

    def astuple(self):
        return QuestionDTO(self.uuid, self.text, [i.astuple() for i in self.choices.all()])


class QuestionChoice(models.Model):
    """ChoiceDTO Database Model"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    uuid = models.CharField(max_length=10)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField()

    def __repr__(self):
        return "QuestionChoice({self.uuid}, {self.text}, {self.is_correct})".format(self=self)

    def __str__(self):
        return self.__repr__()

    @classmethod
    def create(cls, obj: ChoiceDTO, question):
        question_choice = cls(
            uuid=obj.uuid, text=obj.text, is_correct=obj.is_correct, question=question
        )
        question_choice.save()
        return question_choice

    def astuple(self):
        return ChoiceDTO(self.uuid, self.text, self.is_correct)


class AnswerQuiz(models.Model):
    """AnswersDTO Database Model"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.OneToOneField(Quiz, on_delete=models.PROTECT, related_name="answers_quiz")
    score = models.FloatField(blank=True, null=True)
    finished = models.BooleanField(default=False)

    def __repr__(self):
        return "AnswerQuiz({self.score}, {self.finished})".format(self=self)

    def __str__(self):
        return self.__repr__()

    @property
    def questions_uuid(self):
        return self.answers.values_list("answer_quiz")

    @classmethod
    def start_quiz(cls, user, slug_quiz):
        try:
            quiz = Quiz.objects.get(slug=slug_quiz)
        except Quiz.DoesNotExist as e:  # pylint: disable=invalid-name
            raise ValueError(f"slug_quiz: '{slug_quiz}' не является валидным") from e
        instanse = cls(user=user, quiz=quiz)
        instanse.save()
        return instanse

    def get_question(self):
        return (
            self.quiz.questions.unanswered(self.questions_uuid)  # pylint: disable=no-member
            .first()
            .astuple()
        )

    def get_prev_question(self):
        return (
            self.quiz.questions.answered(self.questions_uuid)  # pylint: disable=no-member
            .last()
            .astuple()
        )

    def post_answer(self, answer: AnswerDTO):
        pass


class Answer(models.Model):
    """AnswerDTO Database Model"""

    answer_quiz = models.ForeignKey(AnswerQuiz, on_delete=models.CASCADE, related_name="answers")
    question_uuid = models.CharField(max_length=10)

    def __repr__(self):
        return "Answer({self.question_uuid})".format(self=self)

    def __str__(self):
        return self.__repr__()

    @classmethod
    def create(cls, obj: ChoiceDTO, question):
        question_choice = cls(
            uuid=obj.uuid, text=obj.text, is_correct=obj.is_correct, question=question
        )
        question_choice.save()
        return question_choice


class AnswerChoice(models.Model):
    """AnswerDTO.choices Database Model"""

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=255)

    def __repr__(self):
        return "AnswerChoice({self.text})".format(self=self)

    def __str__(self):
        return self.__repr__()
