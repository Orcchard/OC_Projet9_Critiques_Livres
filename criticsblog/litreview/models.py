from django.db import models
from django.conf import settings


class Ticket(models.Model):
    """missing"""
    pass


class Review(models.Model):
    """Missing"""
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} by {self.user} - {self.time_created}'

