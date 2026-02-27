from django.contrib import admin


# Register your models here.
from .models import UserFollows  # Ajouter plus tard Ticket et Review

admin.site.register(UserFollows)
