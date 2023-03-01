from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class Student(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name or self.email.split("@")[0]

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return None

    @property
    def short_name(self):
        return self.first_name or self.email


class Question(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class Test(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(auto_now=True)
    questions = models.ManyToManyField(Question)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.date}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_answer


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answer)
    is_submitted = models.BooleanField(default=False)

    def get_score(self):
        total_questions = self.test.questions.count()
        total_correct = self.answers.filter(is_correct=True).count()
        score = (total_correct / total_questions) * 100
        return score

    def __str__(self):
        return f"{self.test.name} - {self.test.date} - {self.test.time}"


class Nota(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.test} - {self.score}"


class Quiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    answers = models.ManyToManyField(Answer)

    def get_score(self):
        total_questions = self.questions.count()
        total_correct = self.questions.filter(
            answer__is_correct=True, answer__in=self.answers.all()
        ).count()
        score = (total_correct / total_questions) * 100
        return score

    def __str__(self):
        return f"{self.student} - {self.test}"
