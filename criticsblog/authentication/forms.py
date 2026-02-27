from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from . import models


class SignUpForm(UserCreationForm):
    """Missing"""
    class Meta(UserCreationForm.Meta):
        """Missing"""
        model = get_user_model()
        fields = ('username',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(
        max_length=63, widget=forms.PasswordInput, label='Mot de passe'
    )
