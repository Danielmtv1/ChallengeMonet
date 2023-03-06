from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Student
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
        )
