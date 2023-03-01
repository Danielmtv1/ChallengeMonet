from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Permission,
    Group,
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

    def create_staffuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        group, created = Group.objects.get_or_create(name="students")
        if created:
            print("Created group 'students'")
        user.groups.add(group)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Student(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name="student_groups")
    user_permissions = models.ManyToManyField(
        Permission, related_name="student_user_permissions"
    )

    objects = StudentManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "student"
        verbose_name_plural = "students"

    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return None

    def short_name(self):
        return self.first_name or self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perm(self, app_Label):
        return True

    def __str__(self):
        return f"{self.email}"


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


class StudentAnswer(models.Model):
    # student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    answers = models.CharField(max_length=30, blank=True)
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.test.name} - {self.test.date} - {self.test.time}"


class Nota(models.Model):
    # student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" - {self.test} - {self.score}"  # {self.student}"
