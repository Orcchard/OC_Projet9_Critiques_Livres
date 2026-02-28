from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models


@login_required
def newticket_page(request):
    """Vue pour créer un nouveau ticket. 
    Accessible uniquement aux utilisateurs connectés."""

    if request.method == 'POST':
        form = forms.CreateTicket()
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
