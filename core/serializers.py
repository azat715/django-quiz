from rest_framework import serializers

from core.models import Quiz, Question, QuestionChoice


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"


class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    choices = QuestionChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = "__all__"
