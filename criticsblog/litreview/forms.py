from django import forms
from . import models


MIN_RATING = 1
MAX_RATING = 5
DEFAULT_STARS = 3
RATING_CHOICES = [(i, f"-{i}") for i in range(MIN_RATING, MAX_RATING + 1)]


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
    body = forms.CharField(
        label="Commentaire", max_length=8192, widget=forms.Textarea,
        required=True
        )
    rating = forms.ChoiceField(
        label="Notez ce livre",
        initial=DEFAULT_STARS,
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'inline'}),
        required=True,
        )

    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]
# 