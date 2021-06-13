from rest_framework import serializers

from core.models import (AnswerChoice, AnswerQuiz, Question, QuestionChoice,
                         Quiz)
from quiz.services import AnswerDTO


class QuizSerializer(serializers.ModelSerializer):
    finished = serializers.BooleanField(required=False, default=False)

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


class AnswerQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerQuiz
        exclude = ["user"]
        depth = 1


class ChoiceDTOSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    text = serializers.CharField()
    is_correct = serializers.HiddenField(default="Hidden")

    def create(self, validated_data):
        raise NotImplementedError("ChoiceDTOSerializer не реализовано create")


class QuestionDTOSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    text = serializers.CharField()
    choices = ChoiceDTOSerializer(many=True)

    def create(self, validated_data):
        raise NotImplementedError("QuestionDTOSerializer не реализовано create")


class AnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = "__all__"


class AnswerSerializer(serializers.Serializer):
    question_uuid = serializers.CharField()
    choices = AnswerChoiceSerializer(many=True)

    def create(self, validated_data):
        raise NotImplementedError("AnswerSerializer не реализовано create")


class AnswerPOSTSerializer(serializers.Serializer):
    question_uuid = serializers.CharField()
    choices = serializers.ListField(child=serializers.CharField(), allow_empty=False)

    def create(self, validated_data):
        choices = validated_data.pop("choices")
        answer = AnswerDTO(validated_data["question_uuid"], choices)
        return answer

    def update(self, instance, validated_data):
        raise NotImplementedError("AnswerPOSTSerializer не реализовано update")
