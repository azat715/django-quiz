from django.shortcuts import render
from django.db.models import F
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from core.models import AnswerQuiz, Quiz, Question
from core.serializers import (
    QuizSerializer,
    AnswerQuizSerializer,
    QuestionDTOSerializer,
    AnswerSerializer,
    AnswerPOSTSerializer,
)


@api_view()
@authentication_classes([SessionAuthentication])
@permission_classes([AllowAny])
def quizzes(request):
    if request.user.is_authenticated:
        queryset = Quiz.objects.annotate(finished=F("answers_quiz__finished"))
        serializer = QuizSerializer(queryset, many=True)
        return Response(serializer.data)
    else:
        queryset = Quiz.objects.all()
        serializer = QuizSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(["GET", "POST"])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def quizzes_started(request):
    if request.method == "GET":
        queryset = Quiz.objects.filter(answers_quiz__user=request.user).exclude(
            answers_quiz__finished=True
        )
        serializer = QuizSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        try:
            if AnswerQuiz.objects.filter(
                user=request.user, quiz__uuid=request.data.get("uuid")
            ).exists():
                return Response(
                    {"status": "Викторина уже пройдена"}, status=status.HTTP_400_BAD_REQUEST
                )
            answer = AnswerQuiz.start_quiz(user=request.user, uuid_quiz=request.data.get("uuid"))
            serializer = AnswerQuizSerializer(answer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view()
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def quizzes_finished(request):
    queryset = Quiz.objects.filter(answers_quiz__user=request.user).filter(
        answers_quiz__finished=True
    )
    serializer = QuizSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def questions(request, slug):
    if request.method == "GET":
        try:
            question = AnswerQuiz.objects.get(quiz__slug=slug, user=request.user).get_question()
        except StopIteration:
            return Response({"status": "the questions are over"}, status=status.HTTP_404_NOT_FOUND)
        except AnswerQuiz.DoesNotExist:
            return Response({"status": "quiz not started"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = QuestionDTOSerializer(question)
            return Response(serializer.data)
    elif request.method == "POST":
        answer_quiz = AnswerQuiz.objects.get(quiz__slug=slug, user=request.user)
        serializer = AnswerPOSTSerializer(data=request.data)
        if serializer.is_valid():
            answer = serializer.save()
            res = answer_quiz.post_answer(answer)
            serializer_response = AnswerSerializer(res)
            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH"])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def questions_prev(request, slug):
    if request.method == "GET":
        question = AnswerQuiz.objects.get(quiz__slug=slug, user=request.user).get_prev_question()
        serializer = QuestionDTOSerializer(question)
        return Response(serializer.data)
    elif request.method == "PATCH":
        answer_quiz = AnswerQuiz.objects.get(quiz__slug=slug, user=request.user)
        serializer = AnswerPOSTSerializer(data=request.data)
        if serializer.is_valid():
            answer = serializer.save()
            answer_quiz.update_prev_answer(answer)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def quiz_score(request, slug):
    answer_quiz = AnswerQuiz.objects.get(quiz__slug=slug, user=request.user)
    if Question.objects.unanswered(slug=slug, uuids=answer_quiz.questions_uuid).exists():
        return Response({"status": "questions are not over yet"}, status=status.HTTP_404_NOT_FOUND)
    if not answer_quiz.score:
        answer_quiz.get_score()
        answer_quiz.finished = True
        answer_quiz.save()
    return Response({"score": answer_quiz.score})
