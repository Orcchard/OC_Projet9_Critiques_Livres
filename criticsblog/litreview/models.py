from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
# from .models import Review


class Ticket(models.Model):
    """missing"""
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Champ image avec chemin d'accès organisé
    image = models.ImageField(
        upload_to='ticket_images/',  # Tous les fichiers seront stockés dans.
        # sous-dossier MEDIA_ROOT
        null=True,
        blank=True
    )
    time_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title} by {self.user} - {self.time_created}'
    #  Vérification des droits

    def has_review(self):
        """Vérifie si on a déjà posté une review sur ce ticket"""
        # pylint: disable=no-member
        return self.review_set.exists()


class Review(models.Model):
    """Missing"""
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=timezone.now)
    headline = models.CharField(max_length=128)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )# garanti que la notre est entre 1 et 5
    body = models.TextField(max_length=8192, blank=True)

    def __str__(self):
        return f'{self.headline} by {self.user} - {self.time_created}'
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ticket', 'user'],
                name='unique_review_per_user_per_ticket'
            )
        ]
