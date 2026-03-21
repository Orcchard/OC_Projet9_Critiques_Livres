from django.shortcuts import render, get_object_or_404
from litreview.models import Ticket, Review
from .forms import CreateTicket, CreateReview
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models


@login_required
def newticket_page(request):
    """Vue pour créer un nouveau ticket.
    Accessible uniquement aux utilisateurs connectés."""

    if request.method == 'POST':
        # créer une instance de notre formulaire et le remplir des données POST
        form = forms.CreateTicket(request.POST, request.FILES)
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
    form_review = forms.CreateReview(request.POST)
    if request.method == 'POST' and form_review.is_valid():
        review = form_review.save(commit=False)
        review.ticket = ticket
        review.user = request.user
        review.save()
        return redirect('ticketlist')
    # GET ou formulaire invalide → affichage du ticket + formulaire review
    context = {
        'ticket': ticket,         # pour afficher titre, description, etc.
        'review_form': form_review,
    }
    return render(request, 'litreview/newreview.html', context)


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


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(
        request, 'tickets/ticketdetail.html', {'ticket': ticket}
        )
