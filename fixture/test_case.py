from typing import List

from django.contrib.auth.models import User

from core.models import AnswerQuiz, Question, QuestionChoice, Quiz
from quiz.dto import AnswerDTO, AnswersDTO, ChoiceDTO, QuestionDTO, QuizDTO


user = User.objects.create_user("test_user", "lennon@thebeatles.com", "123")
user.save()

choices: List[ChoiceDTO] = [
    ChoiceDTO("1-1-1", "An elephant", True),
    ChoiceDTO("1-1-2", "A mouse", False),
]
questions: List[QuestionDTO] = [QuestionDTO("1-1", "Who is bigger?", choices)]
quiz: QuizDTO = QuizDTO("1", "Animals", questions)

quiz_db = Quiz.create(quiz)
question_db = Question.create(questions[0], quiz_db)
QuestionChoice.create(choices[0], question_db)
QuestionChoice.create(choices[1], question_db)

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
quiz: QuizDTO = QuizDTO("2", "Test", questions)

quiz_db = Quiz.create(quiz)

for question in quiz[2]:
    q = Question.create(question, quiz_db)
    for choice in question[2]:
        QuestionChoice.create(choice, q)
