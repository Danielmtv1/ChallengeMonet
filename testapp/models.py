from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


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
