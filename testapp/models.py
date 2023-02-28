from django.db import models
from django.contrib.auth.models import (
    User,
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class StudentManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("email is required")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Student(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = StudentManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        return self.email

    class Meta:
        verbose_name = "student"
        verbose_name_plural = "students"


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
    active = models.BooleanField("realizado", default=False)

    def __str__(self):
        return f"{self.name} - {self.date}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_Answer = models.CharField(max_length=100)
    answer_correct = models.BooleanField("Correct answer", default=False)

    def __str__(self):
        return self.option_Answer


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    answer = models.ManyToManyField(Answer)
    is_submitted = models.BooleanField(default=False)

    def get_score(self):
        total_questions = self.test.questions.count()
        total_correct = 0

        for answer in self.answer.all():
            if answer.answer_correct:
                total_correct += 1
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
