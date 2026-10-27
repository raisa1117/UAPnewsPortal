from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from .forms import RegisterForm

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        login(request, form.save())
        messages.success(request, "Welcome to the portal.")
        return redirect("home")
    return render(request, "registration/register.html", {"form": form})
