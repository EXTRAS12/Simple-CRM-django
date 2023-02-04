from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите логин",
                "class": "w-full my-4 py-4 px-6 rounded-xl bg-gray-100",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Введите пароль",
                "class": "w-full my-4 py-4 px-6 rounded-xl bg-gray-100",
            }
        )
    )


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите логин",
                "class": "w-full my-4 bg-gray-100 py-4 px-6 rounded-xl",
            }
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Введите email",
                "class": "w-full my-4 bg-gray-100 py-4 px-6 rounded-xl",
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Введите пароль",
                "class": "w-full my-4 bg-gray-100 py-4 px-6 rounded-xl",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Повторите пароль",
                "class": "w-full my-4 bg-gray-100 py-4 px-6 rounded-xl",
            }
        )
    )
