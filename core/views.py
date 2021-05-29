from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions

from core.models import Quiz
from core.serializers import QuizSerializer


@api_view()
@permission_classes((permissions.AllowAny,))
# @permission_classes([IsAuthenticated])
def get_quizzes(request):
    queryset = Quiz.objects.all()
    serializer = QuizSerializer(queryset, many=True)
    return Response(serializer.data)
