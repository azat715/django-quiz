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

# Вопросы про Python

choices_1: List[ChoiceDTO] = [
    ChoiceDTO("3-1-1", "A. function", False),
    ChoiceDTO("3-1-2", "B. def", True),
    ChoiceDTO("3-1-3", "C. func", False),
    ChoiceDTO("3-1-4", "D. procedure", False),
]
questions: List[QuestionDTO] = [
    QuestionDTO(
        "3-1", "Вопрос 1. С помощью какого ключевого слова объявляется функция:", choices_1
    )
]

choices_2: List[ChoiceDTO] = [
    ChoiceDTO("3-2-1", "A. Идентичности объектов", True),
    ChoiceDTO("3-2-2", "В. Равенства значений объектов", False),
    ChoiceDTO("3-2-3", "C. Принадлежность объекта экземпляру класса", False),
    ChoiceDTO("3-2-4", "D. Наличие объекта в последовательности", False),
]

questions.append(QuestionDTO("3-2", "Вопрос 2. Оператор is служит для проверки", choices_2))

choices_3: List[ChoiceDTO] = [
    ChoiceDTO("3-3-1", "A. super()", True),
    ChoiceDTO("3-3-2", "B. self", False),
    ChoiceDTO("3-3-3", "C. extends", False),
    ChoiceDTO("3-3-4", "D. @abstractmethod", False),
]

questions.append(
    QuestionDTO(
        "3-3",
        "Вопрос 3. Укажите функцию, возвращающую объект-посредник, который делегирует вызовы метода родительскому или родственному классу",
        choices_3,
    )
)

choices_4: List[ChoiceDTO] = [
    ChoiceDTO("3-4-1", "A. @public", False),
    ChoiceDTO("3-4-2", "B. @private", False),
    ChoiceDTO("3-4-3", "C. @classmethod", True),
    ChoiceDTO("3-4-4", "D. @staticmethod", True),
]

questions.append(
    QuestionDTO(
        "3-4", "Вопрос 4. Укажите ключевые слова для обозначения методов класса:", choices_4
    )
)

choices_5: List[ChoiceDTO] = [
    ChoiceDTO("3-5-1", "A. str", True),
    ChoiceDTO("3-5-2", "B. list", False),
    ChoiceDTO("3-5-3", "C. tuple", True),
    ChoiceDTO("3-5-4", "D. dict", False),
]

questions.append(QuestionDTO("3-5", "Вопрос 5. Укажите неизменяемые типы данных:", choices_5))

quiz: QuizDTO = QuizDTO("3", "Questions Python", questions)

quiz_db = Quiz.create(quiz)

for question in quiz[2]:
    q = Question.create(question, quiz_db)
    for choice in question[2]:
        QuestionChoice.create(choice, q)
