from django.shortcuts import render, get_object_or_404
from litreview.models import Ticket, Review
from .forms import CreateTicket, CreateReview
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models
from itertools import chain
from django.db.models import CharField, Value
from authentication.models import UserFollow

MAX_RATING = 5
MIN_RATING = 1
DEFAULT_STARS = 3


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
    context = {
        'ticket': ticket,         # pour afficher titre, description, etc.
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
def ticket_list_page(request):
    """Affiche toutes les  tickets """
    tickets = Ticket.objects.all().order_by('-time_created')
    return render(request, 'litreview/ticketlist.html', {'tickets': tickets})


@login_required
def review_list_page(request):
    """Affiche toutes les reviews avec leurs tickets associés."""
    tickets = Ticket.objects.prefetch_related(
        'review_set'
        ).order_by('-time_created')
    context = {
        'tickets': tickets
    }
    return render(request, 'litreview/reviewlist.html', context)


def feed(request):
    """Prépare et retourne le flux d'activité (feed) pour le user connecté.

    Le feed contient :
    1. Tous les tickets créés par le user connecté et par les utilisateurs qu'il suit.
    2. Toutes les reviews créées par le user connecté et par les utilisateurs qu'il suit.

    Chaque objet est annoté d'un champ temporaire 'content_type' :
        - 'TICKET' pour les tickets
        - 'REVIEW' pour les reviews

    Les objets sont ensuite fusionnés dans une seule liste et triés par date
    de création décroissante (du plus récent au plus ancien).

    Args:
        request: HttpRequest de Django représentant le user connecté.

    Returns:
        render: Rend le template 'litreview/feed.html' avec le contexte {'posts': posts}."""

    # IDs des utilisateurs suivis
    following_ids = list(UserFollow.objects.filter(
        user=request.user
    ).values_list('followed_user', flat=True))

    # On récupère tous les objets UserFollow
    # où le champ user correspond au user connecté request.user
    # values_list() : permet de récupérer un ou plusieurs champs précis des objets filtrés,
    # plutôt que de récupérer tout l’objet complet.
    # flat=True [2, 5, 9] → une liste plate d’IDs, directement utilisable
    # inclure le user lui-même
    users_ids = following_ids + [request.user.id]  
    # ajoute l’ID du user connecté à la liste

    # tickets (les miens + ceux que je suis)
    tickets = Ticket.objects.filter(
        user__in=users_ids
    )
    # ajouter un champ pour différencier
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    # user__in=users → filtre uniquement les tickets dont le champ user est dans la liste users

    # reviews (les miennes + celles que je suis)
    reviews = Review.objects.filter(user__in=users_ids)

    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    # crées un champ temporaire pour chaque objet

    # fusion + tri date décroissante
    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )
    # chain:Permet de concaténer deux itérables (ici tickets et reviews)
    # sans créer une nouvelle liste temporaire

    rating_range = range(MIN_RATING, MAX_RATING + 1)  # passe le range des étoiles au template
    return render(
        request, 'litreview/feed.html',
        {
            'posts': posts, 'following_ids': following_ids, 'rating_range': rating_range,
        })  # pour le template


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
