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
        form = forms.CreateReview(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # On associe la review à un objet User déjà existant en base.
            review.save()
            return redirect('home')  # remplacer par le nom de la vue cible
    else:
        form = forms.CreateReview()
    return render(request, 'litreview/newreview.html', {'review_form': form})

