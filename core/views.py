from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from core.models import AnswerQuiz, Quiz
from core.serializers import QuizSerializer


@api_view()
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_quizzes(request):
    queryset = Quiz.objects.all()
    serializer = QuizSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def start_quiz(request):
    quiz_uuid = request.data.get("quiz_uuid")
    if Quiz.objects.filter(uuid=quiz_uuid).exists():
        AnswerQuiz(request.user, quiz_uuid).save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)
