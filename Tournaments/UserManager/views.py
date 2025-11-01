from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import SignUp, Login

# Create your views here.


def sign_up(request):
    if request.user.is_authenticated:
         return redirect("index")

    form = SignUp(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
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
        login(request=request, user=user)
        messages.add_message(request=request, level=messages.SUCCESS, message="Успішний вхід!")
        return redirect("index")
    return render(request=request, template_name="sign_in.html", context={"form": form})



@login_required(login_url="/users/sign_in/")
def index(request):
    return render(request=request, template_name="index.html")


@login_required(login_url="/users/sign_in/")
def logout_func(request):
    # if request.method == "POST":
        logout(request)
        messages.success(request,"Ви успішно вийшли з системи.")
        return redirect("sign_in")
