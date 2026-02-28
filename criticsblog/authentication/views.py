from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from . import forms


def signup_page(request):
    """Missing"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(
        request, 'authentication/signup.html', context={'form': form})


def login_page(request):
    """Missing"""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # Récupérer les données nettoyées
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # return redirect("home")  # ou "accueil" selon votre URL
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                # Identifiants incorrects
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
        else:  # Formulaire invalide (champs manquants, etc.)
            messages.error(request, "Veuillez remplir correctement tous les champs")

    else:
        form = LoginForm()
    return render(request, "authentication/login.html", {"form": form})


@login_required
def home(request):
    return render(request, "authentication/home.html")


def logout_user(request):
    logout(request)
    return redirect("login")
