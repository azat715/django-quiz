from typing import List

from .dto import AnswerDTO, AnswersDTO, ChoiceDTO, QuestionDTO, QuizDTO


class QuizResultService:
    def __init__(self, quiz_dto: QuizDTO, answers_dto: AnswersDTO):
        self.quiz_dto = quiz_dto
        self.answers_dto = answers_dto
        self.count_questions = len(self.quiz_dto.questions)

    @staticmethod
    def check_answer(question: QuestionDTO, answer: AnswerDTO) -> bool:
        """если количество ответов не совпадает с количеством правильных ответов то сразу False
        если хоть один вариант False сразу return False"""
        if question.uuid != answer.question_uuid:
            raise ValueError(
                f"{answer} и {question} не совпадают uuid: {answer.question_uuid} != {question.uuid}"
            )
        if len(answer.choices) != len([i for i in question.choices if i.is_correct]):
            return False
        if not answer.choices:
            raise ValueError(f"{answer} не содержит ответов")
        for answer_choise in answer.choices:
            for question_choise in question.choices:
                if answer_choise == question_choise.uuid and not question_choise.is_correct:
                    return False
        return True

    def get_result(self) -> float:
        """параллельно итерирую вопросы и ответы и отправляю пару вопрос ответ в check_answer,
        если return True то добавляю count_correct единицу
        результат деление правильных ответов на общее количество вопросов округленное до 2
        """
        if self.quiz_dto.uuid != self.answers_dto.quiz_uuid:
            raise ValueError(f"{self.quiz_dto} и {self.answers_dto} не совпадают uuid")
        count_correct = 0
        for question, answer in zip(self.quiz_dto.questions, self.answers_dto.answers):
            if self.check_answer(question, answer):
                count_correct += 1
        return round(count_correct / self.count_questions, 2)
