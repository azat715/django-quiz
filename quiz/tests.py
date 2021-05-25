from typing import List

from django.test import TestCase

from .dto import AnswerDTO, AnswersDTO, ChoiceDTO, QuestionDTO, QuizDTO
from .services import QuizResultService


class BaseTestCase(TestCase):
    def setUp(self):
        choices: List[ChoiceDTO] = [
            ChoiceDTO("1-1-1", "An elephant", True),
            ChoiceDTO("1-1-2", "A mouse", False),
        ]

        questions: List[QuestionDTO] = [QuestionDTO("1-1", "Who is bigger?", choices)]

        self.quiz_dto = QuizDTO("1", "Animals", questions)

    def test_success_quiz_result(self):
        answers: List[AnswerDTO] = [AnswerDTO("1-1", ["1-1-1"])]

        answers_dto = AnswersDTO("1", answers)

        quiz_result_service = QuizResultService(self.quiz_dto, answers_dto)

        self.assertEqual(quiz_result_service.get_result(), 1.00)

    def test_failure_quiz_result(self):
        answers: List[AnswerDTO] = [AnswerDTO("1-1", ["1-1-2"])]

        answers_dto = AnswersDTO("1", answers)

        quiz_result_service = QuizResultService(self.quiz_dto, answers_dto)

        self.assertEqual(quiz_result_service.get_result(), 0.00)


class ExtendedTestCase(TestCase):
    """Пример расчета результатов"""

    def setUp(self):
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
        self.quiz_dto = QuizDTO("2", "Tест", questions)

    def test_case_1(self):
        answers: List[AnswerDTO] = [
            AnswerDTO("2-1", ["2-1-1"]),
            AnswerDTO("2-2", ["2-2-2", "2-2-3"]),
            AnswerDTO("2-3", ["2-3-4"]),
        ]
        answers_dto = AnswersDTO("2", answers)

        quiz_result_service = QuizResultService(self.quiz_dto, answers_dto)

        self.assertEqual(quiz_result_service.get_result(), 1.00)

    def test_case_2(self):
        answers: List[AnswerDTO] = [
            AnswerDTO("2-1", ["2-1-1"]),
            AnswerDTO("2-2", ["2-2-2"]),
            AnswerDTO("2-3", ["2-3-4"]),
        ]
        answers_dto = AnswersDTO("2", answers)

        quiz_result_service = QuizResultService(self.quiz_dto, answers_dto)

        self.assertEqual(quiz_result_service.get_result(), 0.67)

    def test_case_3(self):
        answers: List[AnswerDTO] = [
            AnswerDTO("2-1", ["2-1-1"]),
            AnswerDTO("2-2", ["2-2-1"]),
            AnswerDTO("2-3", ["2-3-1"]),
        ]
        answers_dto = AnswersDTO("2", answers)

        quiz_result_service = QuizResultService(self.quiz_dto, answers_dto)

        self.assertEqual(quiz_result_service.get_result(), 0.33)

    def test_case_4(self):
        answers: List[AnswerDTO] = [
            AnswerDTO("2-1", ["2-1-1"]),
            AnswerDTO("2-2", ["2-2-1", "2-2-2", "2-2-3"]),
            AnswerDTO("2-3", ["2-3-4"]),
        ]
        answers_dto = AnswersDTO("2", answers)

        quiz_result_service = QuizResultService(self.quiz_dto, answers_dto)

        self.assertEqual(quiz_result_service.get_result(), 0.67)

    def test_case_5(self):
        answers: List[AnswerDTO] = [
            AnswerDTO("2-1", ["2-1-1", "2-1-4"]),
            AnswerDTO("2-2", ["2-2-2", "2-2-3"]),
            AnswerDTO("2-3", ["2-3-4"]),
        ]
        answers_dto = AnswersDTO("2", answers)

        quiz_result_service = QuizResultService(self.quiz_dto, answers_dto)

        self.assertEqual(quiz_result_service.get_result(), 0.67)

    def test_equal_uuid(self):
        answers: List[AnswerDTO] = [
            AnswerDTO("3-1", ["2-3-4"]),
        ]
        answers_dto = AnswersDTO("2", answers)
        quiz_result_service = QuizResultService(self.quiz_dto, answers_dto)
        with self.assertRaises(ValueError):
            self.assertEqual(quiz_result_service.get_result(), 0.67)
