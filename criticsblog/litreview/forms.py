from django import forms

from . import models


class CreateTicket(forms.ModelForm):
    """Missing"""
    title = forms.CharField(label="Titre du livre", max_length=128, required=True)
    description = forms.CharField(max_length=2048, widget=forms.Textarea, required=True)
    image = forms.ImageField(required=True)

    class Meta:
        """Missing"""
        model = models.Ticket
        fields = ["title", "description", "image"]
        labels = {
            'image': 'Télécharger fichier',
        }


class CreateReview(forms.ModelForm):
    headline = forms.CharField(label="Titre", required=True)
    body = forms.CharField(label="Commentaire", max_length=8192, widget=forms.Textarea, required=True)
    rating = forms.ChoiceField(
        initial=3,
        label="Notez ce livre",
        widget=forms.RadioSelect(attrs={'class': 'inline'}),
        required=True,
        choices=(
            (1, "-1"),
            (2, "-2"),
            (3, "-3"),
            (4, "-4"),
            (5, "-5"))
        )

    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]
