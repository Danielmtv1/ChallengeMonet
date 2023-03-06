from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Student, StudentAnswer, Test, Question
from .serializers import StudentAnswerSerializer
from datetime import datetime


class StudentSignupViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student_data = {
            "email": "test@example.com",
            "password": "test_password",
            "first_name": "Test",
            "last_name": "User",
        }
        self.url = reverse("signup")

    def test_create_student(self):
        response = self.client.post(self.url, self.student_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        student = Student.objects.first()
        self.assertEqual(student.email, self.student_data["email"])
        self.assertEqual(student.first_name, self.student_data["first_name"])
        self.assertEqual(student.last_name, self.student_data["last_name"])
        self.assertTrue(student.check_password(self.student_data["password"]))
        self.assertTrue(student.is_staff)
        self.assertFalse(student.is_superuser)
        self.assertTrue(student.is_active)


class AnswerStudentViewSetTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("Student_Answers")
        self.user = Student.objects.create_user(
            email="testuser@mail.com", password="testpass"
        )
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"email": self.user.email, "password": "testpass"},
            format="json",
        )
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        self.test = Test.objects.create(name="test", date=datetime.now().date())
        self.question = Question.objects.create(test=self.test, text="test question")

    def test_create_student_answer(self):
        data = {"test_id": 1, "question": 1, "answers": "answer test"}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        answer = StudentAnswer.objects.get(pk=response.data["id"])
        serializer = StudentAnswerSerializer(answer)
        self.assertEqual(serializer.data, response.data)
