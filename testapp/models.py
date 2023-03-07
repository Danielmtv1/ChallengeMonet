from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Permission,
    Group,
)
from django.db import models


class StudentManager(BaseUserManager):
    """
    A custom user manager for the Student model.

    This manager provides methods for creating Student users, staff users, and superusers.
    """

    def create_user(self, email, password=None):
        """
        Creates and saves a Student user with the given email and password.

        Args:
            email (str): The email address of the user.
            password (str, optional): The password for the user. If not provided, a random password will be generated.

        Returns:
            Student: The newly created Student user.

        Raises:
            ValueError: If email is not provided.
        """
        if not email:
            raise ValueError("email is required")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user.

        Returns:
            User: The newly created staff user.

        Raises:
            ValueError: If email is not provided.
        """
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
        """
        Creates and saves a superuser with the given email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user.

        Returns:
            User: The newly created superuser.

        Raises:
            ValueError: If email is not provided.
        """

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Student(AbstractBaseUser, PermissionsMixin):
    """
    A custom user model for representing a Student.

    This model extends the AbstractBaseUser and PermissionsMixin classes, and provides fields for email, first name, last name,
    and group and permission associations. It also defines several methods for interacting with student objects.

    Attributes:
        email (str): The email address of the student. This field is unique.
        first_name (str): The first name of the student.
        last_name (str): The last name of the student.
        is_active (bool): A boolean indicating whether the student is currently active.
        is_staff (bool): A boolean indicating whether the student is a member of the staff.
        is_superuser (bool): A boolean indicating whether the student is a superuser.
        groups (ManyToManyField): A many-to-many relationship between students and groups.
        user_permissions (ManyToManyField): A many-to-many relationship between students and permissions.
        objects (StudentManager): The manager for creating and manipulating student objects.
        USERNAME_FIELD (str): The name of the field that serves as the unique identifier for a student (in this case, 'email').

    Methods:
        full_name(): Returns the full name of the student, combining the first and last name.
        short_name(): Returns a shortened name for the student, using the first name if available, or the email address otherwise.
        has_perm(perm, obj=None): Determines whether the student has the specified permission (in this case, only staff members can view student answers).
        has_module_perms(app_label): Determines whether the student has permissions to access all modules.

    Meta:
        verbose_name (str): The verbose name of a single student object.
        verbose_name_plural (str): The verbose name of the collection of student objects.
    """

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

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
        if self.is_staff and not self.is_superuser:
            if perm == "testapp.view_studentanswer":
                return True
        else:
            return True

    def has_module_perms(self, app_label):
        return True


class Test(models.Model):
    """A model representing a test.

    Attributes:
        name (str): The name of the test.
        description (str): A description of the test.
        date (date): The date the test will be administered.
        time (time): The time the test was last updated.
        is_active (bool): Whether the test is currently active.

    Methods:
        __str__: Returns a string representation of the test, including its name and date.
    """

    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.date}"


class Question(models.Model):
    """A model representing a question in a test.

    Attributes:
        test (Test): The test to which this question belongs.
        text (str): The text of the question.

    Methods:
        __str__: Returns the text of the question as a string.
    """

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

    def __str__(self):
        return self.text


class StudentAnswer(models.Model):
    """A model representing a student's answer to a question.

    Attributes:
        student (Student): The student who provided the answer.
        question (Question): The question to which the student provided an answer.
        answers (str): The answer provided by the student.

    Methods:
        __str__: Returns a string representation of the student who provided the answer.
    """

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    answers = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.student}"
