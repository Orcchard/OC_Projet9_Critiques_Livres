from django.shortcuts import render
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
            return redirect('home')  # remplacer par le nom de la vue cible
        else:
            form = forms.CreateTicket()
        return render(request, 'litreview/newticket.html', {'ticket_form': form})

@login_required
def newreview_page(request):
    """Vue pour créer une nouvelle critique. 
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
        # Initialisation des formulaires pour GET
        form_ticket = forms.CreateTicket()
        form_review = forms.CreateReview()

        # affichage des formulaires (GET ou POST invalide)
    context = {'ticket_form': form_ticket, 'review_form': form_review}
    return render(request, 'litreview/newreview.html', context)
