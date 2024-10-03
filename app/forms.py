from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
            "id": "form3Example1cg",
            "class": "form-control form-control-lg"
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "id": "form3Example3cg",
        "class": "form-control form-control-lg"
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "id": "form3Example4cg",
        "class": "form-control form-control-lg"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "id": "form3Example4cdg",
        "class": "form-control form-control-lg"
    }))

    class Meta:
        model = User
        fields = ('username', 'email')


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
            "id": "form2Example1",
            "class": "form-control"
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "id": "form2Example2",
        "class": "form-control"
    }))