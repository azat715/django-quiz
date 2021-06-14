from itertools import groupby

from django.conf import settings
from django.db import models
from django.utils.text import slugify

from quiz.dto import AnswerDTO, AnswersDTO, ChoiceDTO, QuestionDTO, QuizDTO
from quiz.services import QuizResultService


class Quiz(models.Model):
    """QuizDTO Database Model"""

    uuid = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    slug = models.SlugField(null=False, unique=True)

    def __repr__(self) -> str:
        return "Quiz({self.uuid}, {self.title}, {self.slug})".format(self=self)

    def __str__(self) -> str:
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

    def astuple(self) -> QuizDTO:
        return QuizDTO(self.uuid, self.title, [i.astuple() for i in self.questions.all()])


class QuestionManager(models.Manager):
    def unanswered(self, slug, uuids):
        return super().get_queryset().filter(quiz__slug=slug).exclude(uuid__in=uuids)

    def answered(self, slug, uuids):
        return super().get_queryset().filter(quiz__slug=slug).filter(uuid__in=uuids)


class Question(models.Model):
    """QuestionDTO Database Model"""

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    uuid = models.CharField(max_length=10)
    text = models.CharField(max_length=255)

    objects = QuestionManager()

    def __repr__(self) -> str:
        return "Question({self.uuid}, {self.text})".format(self=self)

    def __str__(self) -> str:
        return self.__repr__()

    @classmethod
    def create(cls, obj: QuestionDTO, quiz):
        question = cls(uuid=obj.uuid, text=obj.text, quiz=quiz)
        question.save()
        return question

    def astuple(self) -> QuestionDTO:
        return QuestionDTO(self.uuid, self.text, [i.astuple() for i in self.choices.all()])


class QuestionChoice(models.Model):
    """ChoiceDTO Database Model"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    uuid = models.CharField(max_length=10)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField()

    def __repr__(self) -> str:
        return "QuestionChoice({self.uuid}, {self.text}, {self.is_correct})".format(self=self)

    def __str__(self) -> str:
        return self.__repr__()

    @classmethod
    def create(cls, obj: ChoiceDTO, question):
        question_choice = cls(
            uuid=obj.uuid, text=obj.text, is_correct=obj.is_correct, question=question
        )
        question_choice.save()
        return question_choice

    def astuple(self) -> QuestionDTO:
        return ChoiceDTO(self.uuid, self.text, self.is_correct)


class AnswerQuiz(models.Model):
    """AnswersDTO Database Model"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT, related_name="answers_quiz")
    score = models.FloatField(blank=True, null=True)
    finished = models.BooleanField(default=False)

    def __repr__(self) -> str:
        return "AnswerQuiz({self.score}, {self.finished})".format(self=self)

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def questions_uuid(self):
        return self.answers.values_list("question_uuid")

    @classmethod
    def start_quiz(cls, user, uuid_quiz: str):
        try:
            quiz = Quiz.objects.get(uuid=uuid_quiz)
        except Quiz.DoesNotExist as e:  # pylint: disable=invalid-name
            raise ValueError(f"uuid_quiz: '{uuid_quiz}' не является валидным") from e
        instanse = cls(user=user, quiz=quiz)
        instanse.save()
        return instanse

    def get_question(self) -> QuestionDTO:
        if Question.objects.unanswered(self.quiz.slug, self.questions_uuid).exists():
            return (
                Question.objects.unanswered(self.quiz.slug, self.questions_uuid).first().astuple()
            )
        else:
            raise StopIteration("Вопросы кончились")

    def get_prev_question(self) -> QuestionDTO:
        return Question.objects.answered(self.quiz.slug, self.questions_uuid).last().astuple()

    def post_answer(self, obj: AnswerDTO):
        answer = Answer.create(obj, self)
        for choice in obj.choices:
            instanse = AnswerChoice(text=choice, answer=answer)
            instanse.save()
        return answer

    def update_prev_answer(self, obj: AnswerDTO):
        Answer.objects.filter(answer_quiz=self).last().delete()
        self.post_answer(obj)

    def get_score(self):
        queryset = QuestionChoice.objects.select_related("question").filter(
            question__quiz=self.quiz
        )
        questions = []
        for key, group in groupby(queryset, key=lambda x: x.question):
            choices = []
            for choice in group:
                choices.append(ChoiceDTO(choice.uuid, choice.text, choice.is_correct))
            questions.append(QuestionDTO(key.uuid, key.text, choices))

        quiz_dto: QuizDTO = QuizDTO(self.quiz.uuid, self.quiz.title, questions)
        answers_dto = self.astuple()  # необходимо выделить таблицу AnswersDTO как Quiz
        calc = QuizResultService(quiz_dto, answers_dto)
        self.score = calc.get_result()
        return self.score

    def astuple(self) -> AnswerDTO:
        return AnswersDTO(self.quiz.uuid, [i.astuple() for i in self.answers.all()])


class Answer(models.Model):
    """AnswerDTO Database Model"""

    answer_quiz = models.ForeignKey(AnswerQuiz, on_delete=models.CASCADE, related_name="answers")
    question_uuid = models.CharField(max_length=10)

    def __repr__(self) -> str:
        return "Answer({self.question_uuid})".format(self=self)

    def __str__(self) -> str:
        return self.__repr__()

    @classmethod
    def create(cls, obj: AnswerDTO, answer_quiz):
        answer = cls(answer_quiz=answer_quiz, question_uuid=obj.question_uuid)
        answer.save()
        return answer

    def astuple(self) -> AnswerDTO:
        return AnswerDTO(self.question_uuid, [i.text for i in self.choices.all()])


class AnswerChoice(models.Model):
    """AnswerDTO.choices Database Model"""

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=255)

    def __repr__(self) -> str:
        return "AnswerChoice({self.text})".format(self=self)

    def __str__(self) -> str:
        return self.__repr__()
