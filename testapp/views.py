from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import (
    StudentSerializer,
    StudentAnswerSerializer,
    TestSerializer,
    QuestionSerializer,
    QuizSerializer,
)
from rest_framework import status
from rest_framework.decorators import api_view, schema
from rest_framework.schemas import AutoSchema
from .models import Student, Test, Question, StudentAnswer, Quiz
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework.generics import CreateAPIView

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class StudentSignupView(CreateAPIView):
    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        password = validated_data["password"]

        # Validar la contraseña utilizando las reglas de validación de Django
        try:
            password_validation.validate_password(password)
        except password_validation.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        # Encriptar la contraseña utilizando make_password
        validated_data["password"] = make_password(
            password,
            "key",
        )

        # Crear el estudiante y devolver los datos validados
        self.perform_create(serializer)
        data = serializer.data
        data.pop("password")  # Eliminar el campo password
        message = {"message": "Estudiante creado exitosamente."}
        data.update(message)  # Agregar el mensaje de confirmación

        headers = self.get_success_headers(serializer.data)
        return Response(
            data,
            status=status.HTTP_201_CREATED,
        )


class StudentLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({"token": token})
        else:
            return Response({"error": "Credenciales inválidas"}, status=400)


class ProtectedView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"message": "Bienvenido, estudiante!"})


class CustomAutoSchema(AutoSchema):
    def get_link(self, path, method, base_url):
        pass


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ActiveTestList(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    queryset = Test.objects.all()


class QuestionsViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class AnswerStudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentAnswerSerializer
    queryset = StudentAnswer.objects.all()


class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    queryset = StudentAnswer.objects.all()


@api_view(["POST", "GET"])
@schema(CustomAutoSchema())
def viewst(request, *args, **kwargs):
    if request.method == "GET":
        active_test = Test.objects.filter(active=True).first()
        if active_test:
            questions = active_test.questions.all()
            question_data = []
            for question in questions:
                answers = question.answer_set.all()
                answer_data = []
                for answer in answers:
                    answer_data.append(answer.option_Answer)
                question_data.append({"text": question.text, "answers": answer_data})
            return Response({"test_name": active_test.name})
