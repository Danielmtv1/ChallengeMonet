from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers

from .models import Student, StudentAnswer, Test, Question


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


class StudentAnswerSerializer(serializers.ModelSerializer):
    test_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = StudentAnswer
        fields = ["id", "test_id", "question", "answers"]

    def create(self, validated_data):
        user = self.context["request"].user
        student = user if user.is_staff else None
        test_id = validated_data.pop("test_id", None)
        answer = StudentAnswer.objects.create(student=student, **validated_data)
        if test_id is not None:
            test = Test.objects.get(id=test_id)
            answer.test = test
            answer.save()
        return answer


class QuestionSerializer(serializers.ModelSerializer):
    answers = StudentAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "text", "answers")


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ("id", "name", "description", "date", "time", "questions", "is_active")
