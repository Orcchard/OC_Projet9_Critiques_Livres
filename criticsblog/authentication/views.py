from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Applications externes (autres apps du projet)
from litreview.forms import CreateTicket
from litreview.models import Ticket, Review
from .models import UserFollow

# Imports locaux
from .models import UserFollow
from .forms import SignUpForm, LoginForm


User = get_user_model()


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
    users = UserFollow.objects.values_list(
        'user__username',
        'followed_user__username'
    )

    # on aplati + on enlève les doublons
    unique_users = set()
    for u1, u2 in users:
        unique_users.add(u1)
        unique_users.add(u2)

    return render(request, "authentication/home.html", {
        "users": unique_users
    })


def logout_user(request):
    """Missing"""
    logout(request)
    return redirect("login")


def subscribe_page(request):
    """Missing"""
    query = request.GET.get('q') # récupère la valeur tapée dans la barre de recherche
    search_user = None
    # Initialisation de la variable
    if query:     # l'utilisateur a t'il saisi?
        query = query.strip()  # enlève espaces invisibles
        try:
            search_user = User.objects.get(username=query)  # recherche EXACTE
            # empêcher de se rechercher soi-même
            if search_user == request.user:
                search_user = None
        except User.DoesNotExist:
            search_user = None
            messages.warning(request, "Aucun abonné à ce nom.")
    # Utilisateurs que je suis
    following = User.objects.filter(followed_by__user=request.user)
    # followed_by_user:syntaxe de Django ORM pour traverser une relation
    # le double underscore __ clé pour comprendre Django ORM et la façon dont
    # il traverse les relations.
    # ForeignKey / related_name.
    # Donne-moi tous les utilisateurs qui sont suivis par request.user
    # l’utilisateur actuellement connecté qui consulte le feed.

    # Utilisateurs qui me suivent
    followers = User.objects.filter(following__followed_user=request.user)
    # following__followed_user: syntaxe de Django ORM pour traverser
    # une relation ForeignKey / related_name.
    # Donne-moi tous les utilisateurs qui me suivent

    return render(request, "authentication/subscribe.html", {
        'search_user': search_user,
        'following': following,
        'followers': followers,
    })


@login_required
def follow_user_page(request, user_id):
    """But : récupérer l’utilisateur que l’on veut suivre (other_user)
    Si l’utilisateur n’existe pas → renvoie automatiquement 404,
    donc la vue ne plante pas"""
    # utilisateur à suivre
    # pylint: disable=E1101
    other_user = get_object_or_404(User, id=user_id)
    # éviter de se suivre soi-même
    if other_user != request.user:
        # créer la relation si elle n'existe pas encore
        UserFollow.objects.get_or_create(
            user=request.user,
            followed_user=other_user
        )
        return redirect('subscribe')


@login_required
def unfollow_user_page(request, user_id):
    """
    But : permettre à l'utilisateur connecté de ne plus suivre 'other_user'.
    - Vérifie que 'other_user' existe.
    - Empêche de se désuivre soi-même.
    - Supprime la relation si elle existe.
    """
    other_user = get_object_or_404(User, id=user_id)

    # impossible de se désuivre soi-même
    if other_user != request.user:
        # supprimer la relation si elle existe
        # pylint: disable=E1101
        UserFollow.objects.filter(
            user=request.user,
            followed_user=other_user
        ).delete()

    # retour à la page précédente ou accueil
    return redirect('subscribe')
