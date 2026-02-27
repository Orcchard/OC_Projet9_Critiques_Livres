from django.shortcuts import render


def ticket_page(request):
    """Missing"""
    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)
    if request.method == 'POST':
        # créer une instance de notre formulaire et le remplir données POST
        form = (request.POST)
        if form.is_valid():
            print("Ok je peux avancer")
