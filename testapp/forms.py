from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Student


class FormRegister(forms.modelform):
    password = forms.CharField(widget=forms.PasswordInput)
