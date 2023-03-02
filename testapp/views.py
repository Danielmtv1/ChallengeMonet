from rest_framework import status, viewsets, serializers
from rest_framework.generics import CreateAPIView
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


class ProtectedView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"message": "Bienvenido, estudiante!"})


class ActiveTestList(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    queryset = Test.objects.all()

    def retrieve(self, request, pk=None):
        try:
            test = self.get_queryset().get(pk=pk)
            serializer = TestSerializer(test)
            return Response(serializer.data)
        except Test.DoesNotExist:
            return Response(
                {"error": "La prueba no existe."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AnswerStudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentAnswerSerializer
    queryset = StudentAnswer.objects.all()
    permission_classes = [IsAuthenticated]
