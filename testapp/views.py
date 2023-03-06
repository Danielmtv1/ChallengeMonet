from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets, serializers
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from .models import Test, StudentAnswer
from .serializers import (
    StudentSerializer,
    StudentAnswerSerializer,
    TestSerializer,
)


class StudentSignupView(CreateAPIView):
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
    serializer_class = StudentAnswerSerializer
    queryset = StudentAnswer.objects.all()
    permission_classes = [IsAuthenticated]


class ActiveTestList(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    @action(detail=False, methods=["get"])
    def list(self, request):
        queryset = Test.objects.filter(is_active=True)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class TestTakingView(APIView):
    queryset = Test.objects.all()
    permission_classes = (IsAuthenticated,)
    print(IsAuthenticated.has_permission)

    def get(self, test_id):
        tests = Test.objects.get(id=test_id)
        serializer = TestSerializer(tests)
        return Response(serializer.data)
