from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from litreview.models import Ticket, Review
from .models import User, UserFollow
from litreview.forms import CreateTicket
from django import forms

from .forms import SignUpForm, LoginForm


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
                return redirect("home")  # ou "accueil" selon votre URL
            else:
                # Identifiants incorrects
                messages.error(
                    request, "Nom d'utilisateur ou mot de passe incorrect"
                    )
        else:  # Formulaire invalide (champs manquants, etc.)
            messages.error(
                request, "Veuillez remplir correctement tous les champs"
                )

    else:
        form = LoginForm()
    return render(
        request, "authentication/login.html", {"form": form}
        )


@login_required
def home(request):
    # récupère tous les tickets
    return render(request, "authentication/home.html")


def logout_user(request):
    """Missing"""
    logout(request)
    return redirect("login")


def followers_list(request):
    """Missing"""
    followers_relations = request.user.followed_by.all()
    followers = [relation.user for relation in followers_relations]
    return render(request, 'followers_list.html', {
        'followers': followers
    })


def suscribe_page(request):
    """Missing"""
    # Tous les utilisateurs sauf soi-même pour l'interface, un user ne peux s'appeler
    users = User.objects.exclude(id=request.user.id)

    # Utilisateurs que je suis
    # on récupère des utilisateurs (User) à partir de la base de données.
    following = User.objects.filter(followed_by__user=request.user)

    # Utilisateurs qui me suivent
    followers = User.objects.filter(following__followed_user=request.user)
    # followed_by → Related_name que défini dans ton modèle UserFollow :

    return render(request, 'abonnements.html', {
        'users': users,
        'following': following,
        'followers': followers,
    })


def follow_user_page(request, id):
    """Missing"""


def unfollow_user_page(request, id):
    """Missing"""
