from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()

    class Meta:

        model = User
        fields = ['username', 'email','first_name', 'password1', 'password2']
