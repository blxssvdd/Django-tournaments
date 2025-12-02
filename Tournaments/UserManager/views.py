from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from .forms import Login, ProfileUpdateForm, SignUp
from .models import Profile


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("index")

    form = SignUp(data=request.POST or None, files=request.FILES or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        Profile.objects.get_or_create(user=user)
        login(request=request, user=user)
        messages.add_message(request=request, level=messages.SUCCESS, message="Успішна реєстрація!")
        return redirect("index")
    return render(request=request, template_name="sign_up.html", context={"form": form})


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("index")

    form = Login(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        Profile.objects.get_or_create(user=user)
        login(request=request, user=user)
        messages.add_message(request=request, level=messages.SUCCESS, message="Успішний вхід!")
        return redirect("index")
    return render(request=request, template_name="sign_in.html", context={"form": form})


@login_required(login_url="/users/sign_in/")
def index(request):
    return render(request=request, template_name="index.html")


@login_required(login_url="/users/sign_in/")
def logout_func(request):
    logout(request)
    messages.success(request,"Ви успішно вийшли з системи.")
    return redirect("sign_in")


@login_required(login_url="/users/sign_in/")
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(
        request=request,
        template_name="profile_detail.html",
        context={"profile": profile},
    )


@login_required(login_url="/users/sign_in/")
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileUpdateForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=profile,
        user=request.user,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Профіль оновлено.")
        return redirect("profile")
    return render(
        request=request,
        template_name="profile_edit.html",
        context={"form": form, "profile": profile},
    )


@login_required(login_url="/users/sign_in/")
def change_password(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Пароль успішно змінено.")
        return redirect("profile")
    return render(
        request=request,
        template_name="password_change.html",
        context={"form": form},
    )
