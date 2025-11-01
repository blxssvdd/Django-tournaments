from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class SignUp(UserCreationForm):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}), label="Логін", help_text="Обов'язково. До 20 символів. Латинські літери, цифри тільки.")
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}), label="Ім'я")
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}), label="Прізвище")
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={"class": "form-control"}), label="Електронна пошта")
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Пароль")
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Підтвердження пароля")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2",)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class Login(AuthenticationForm):
    username = forms.CharField(label="Логін", widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"}))
