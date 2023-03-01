from django.core.exceptions import ValidationError
from django.core.mail import utils
from django.core.validators import validate_email
from rest_framework import serializers

from .models import Question, Quiz, Student, StudentAnswer, Test


def validate_email_format(email):
    try:
        validate_email(email)
    except ValidationError:
        raise serializers.ValidationError("Invalid email format")
    return email


class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True,
        style={
            "input_type": "password",
            "placeholder": "Password",
            "label": "Password",
        },
    )

    class Meta:
        model = Student
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
        )

    def validate_email(self, value):
        email = validate_email_format(value)
        if Student.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email is already in use")
        return email


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "description",
            "date",
            "time",
            "questions",
            "active",
        )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            "id",
            "text",
        )


class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = (
            "student",
            "test",
            "answer",
        )


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    answers = StudentAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = (
            "student",
            "test",
            "questions",
            "answers",
        )
