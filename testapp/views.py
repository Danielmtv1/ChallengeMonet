from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation
from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import StudentAnswer
from .serializers import StudentSerializer, StudentAnswerSerializer


######-Student Views
class StudentSignupView(CreateAPIView):
    """A view for creating a new student account.

    Attributes:
        serializer_class: The serializer used to validate and deserialize the request data.

    Methods:
        create: Handles POST requests to create a new student account.
    """

    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        password = validated_data["password"]

        try:
            password_validation.validate_password(password)
        except password_validation.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        validated_data["password"] = make_password(
            password,
            "key",
        )

        self.perform_create(serializer)
        data = serializer.data
        data.pop("password")
        message = {"message": "Estudiante creado exitosamente."}
        data.update(message)

        headers = self.get_success_headers(serializer.data)
        return Response(
            data,
            status=status.HTTP_201_CREATED,
        )


class AnswerStudentViewSet(CreateAPIView):
    """A view for creating a student answer to a question.

    Attributes:
        serializer_class: The serializer used to validate and deserialize the request data.
        queryset: The queryset used to retrieve the student answers.
        permission_classes: The permission classes required to access the view.

    Methods:
        create: Handles POST requests to create a new student answer to a question.
    """

    serializer_class = StudentAnswerSerializer
    queryset = StudentAnswer.objects.all()
    permission_classes = [IsAuthenticated]


#### Test Views unavalible
"""class ActiveTestList(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    @action(detail=False, methods=["get"])
    def list(self, request):
        queryset = Test.objects.filter(is_active=True)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)"""
