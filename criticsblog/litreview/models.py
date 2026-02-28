from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Ticket(models.Model):
    """missing"""
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title} by {self.user} - {self.time_created}'


class Review(models.Model):
    """Missing"""
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=timezone.now)
    headline = models.CharField(max_length=128)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    body = models.TextField(max_length=8192, blank=True)

    def __str__(self):
        return f'{self.headline} by {self.user} - {self.time_created}'
