from rest_framework import status, viewsets, serializers

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from .models import Student, Test, StudentAnswer
from .serializers import (
    StudentSerializer,
    StudentAnswerSerializer,
    TestSerializer,
)

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


class StudentLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


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


class AnswerStudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentAnswerSerializer
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
