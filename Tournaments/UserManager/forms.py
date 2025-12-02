from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from captcha.fields import CaptchaField

from .models import Profile


class SignUp(UserCreationForm):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}), label="Логін", help_text="Обов'язково. До 20 символів. Латинські літери, цифри тільки.")
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}), label="Ім'я")
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}), label="Прізвище")
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={"class": "form-control"}), label="Електронна пошта")
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Пароль")
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Підтвердження пароля")
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={"class": "form-control"}), label="Аватар (необов'язково)")
    captcha = CaptchaField(label="Введіть символи", error_messages={"invalid": "Невірні символи"})
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "avatar")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            avatar = self.cleaned_data.get("avatar")
            if avatar:
                profile, _ = Profile.objects.get_or_create(user=user)
                profile.avatar = avatar
                profile.save()
        return user


class Login(AuthenticationForm):
    username = forms.CharField(label="Логін", widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    captcha = CaptchaField(label="Введіть символи", error_messages={"invalid": "Невірні символи"})


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Ім'я",
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Прізвище",
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        label="Електронна пошта",
    )

    class Meta:
        model = Profile
        fields = ("display_name", "bio", "avatar", "first_name", "last_name", "email")
        widgets = {
            "display_name": forms.TextInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "display_name": "Нікнейм (на екрані)",
            "bio": "Про себе",
            "avatar": "Аватар",
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["first_name"].initial = self.user.first_name
        self.fields["last_name"].initial = self.user.last_name
        self.fields["email"].initial = self.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]
        self.user.email = self.cleaned_data["email"]
        if commit:
            self.user.save()
            profile.user = self.user
            profile.save()
        return profile
