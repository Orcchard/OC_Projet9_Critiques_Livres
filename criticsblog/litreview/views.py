from django.shortcuts import render, get_object_or_404, redirect
from authentication.models import UserFollow
from litreview.models import Ticket, Review
from .forms import CreateTicket, CreateReview
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import forms
from itertools import chain
from django.db.models import CharField, Value
from litreview.services import get_users_viewable_tickets, get_users_viewable_reviews


MAX_RATING = 5
MIN_RATING = 1
DEFAULT_STARS = 3
rating_range = range(MIN_RATING, MAX_RATING + 1)


@login_required
def newticket_page(request):
    """Vue pour créer un nouveau ticket.
    Accessible uniquement aux utilisateurs connectés."""

    if request.method == 'POST':
        # créer une instance de notre formulaire et le remplir des données POST
        form = forms.CreateTicket(request.POST, request.FILES)
        # Méthode get qui affiche le formulaire
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')  # redirige vers URL après création d'objet en database
    else:
        form = forms.CreateTicket()
    return render(request, 'litreview/newticket.html', {'ticket_form': form})


@login_required
def newreview_page(request, ticket_id):
    """Crée une review pour un ticket.
    Si ticket_id est fourni, ajoute la review à un ticket existant.
    Sinon, crée un nouveau ticket + review."""
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form_review = forms.CreateReview(request.POST)
        if form_review.is_valid():
            review = form_review.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('feed')
    else:
        form_review = forms.CreateReview()
        # formulaire vide pour GET
        # GET ou formulaire invalide → affichage du ticket + formulaire review
        # Méthode get qui affiche le formulaire
        # pour afficher titre, description, etc.
    context = {
        'ticket': ticket,         
        'review_form': form_review,
    }
    return render(request, 'litreview/newreview.html', context)
    # Méthode get qui affiche le formulaire


@login_required
def create_ticket_and_review_page(request):
    """Vue pour créer une nouvelle critique liée à un ticket vierge.
    Accessible uniquement aux utilisateurs connectés."""
    if request.method == 'POST':
        # créer une instance de notre formulaire et le remplir des données POST
        form_ticket = forms.CreateTicket(request.POST, request.FILES)
        form_review = forms.CreateReview(request.POST)

        # sauvegarde du ticket
        if form_ticket.is_valid() and form_review.is_valid():
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            ticket.reply = True
            ticket.save()

        # sauvegarde de la review
            review = form_review.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('home')
    else:
        # GET → on crée des formulaires vides
        form_ticket = forms.CreateTicket()
        form_review = forms.CreateReview()

    # Toujours renvoyer un HttpResponse pour GET ou POST invalide
    return render(
        request,
        'litreview/ticket-review.html',
        {'ticket_form': form_ticket, 'review_form': form_review}
    )


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    if request.method == 'POST':
        form = CreateTicket(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = CreateTicket(instance=ticket)

    return render(request, 'litreview/edit_ticket.html', {'form': form})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        form = CreateReview(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = CreateReview(instance=review)

    return render(request, 'litreview/edit_review.html', {'form': form})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    if request.method == 'POST':
        ticket.delete()
        return redirect('feed')
    return render(
        request, 'litreview/delete_ticket.html', {'ticket': ticket})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()
        return redirect('feed')
    return render(request, 'litreview/delete_review.html', {'review': review})


@login_required
def feed(request):
    """Affiche le flux des tickets et reviews :
    - de l'utilisateur connecté
    - des utilisateurs qu'il suit
    """

    # tickets visibles
    tickets = get_users_viewable_tickets(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    print(f"TT: {tickets}")

    # reviews visibles
    reviews = get_users_viewable_reviews(request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    print(f"RR: {reviews}")

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True)
    print(f"POSTS: {posts}")

    return render(request, 'litreview/feed.html', {
        "posts": posts,
        "rating_range": rating_range
    })


@login_required
def mypublications(request):
    pass
