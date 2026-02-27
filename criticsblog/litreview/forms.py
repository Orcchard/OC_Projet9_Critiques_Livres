from django import forms

from . import models


class CreateTicket(forms.ModelForm):
    """Missing"""
    title = forms.CharField(label="Title of the book", max_length=128, required=True)
    description = forms.CharField(max_length=2048, widget=forms.Textarea, required=True)
    image = forms.ImageField(required=True)

    class Meta:
        """Missing"""
        model = models.Ticket
        fields = ["title", "description", "image"]
