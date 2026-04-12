from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from typing import TYPE_CHECKING


class UserFollow(models.Model):
    """
        Chaque instance de UserFollow = une relation “user suit followed_user”
        Je ne veux pas juste savoir QUI suit QUI…
        je veux aussi stocker des infos SUR cette relation”.
        le modèle UserFollow permet de stocker des informations propres
        à la relation, qui n’existent ni sur le ticket, ni sur la review
        user → l’utilisateur qui suit quelqu’un
        followed_user → l’utilisateur qui est suivi
        related_name → permet d’accéder à la relation depuis l’autre modèle (User)
    """
    # Chaque relation indique quel utilisateur suit d’autres utilisateurs
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, 
        # ce champ est lié au modèle utilisateur utilisé par le projet
        # ForeignKey vers le modèle User défini dans les paramètres Django

        on_delete=models.CASCADE,
        related_name='following'
    )
    # 'following' : permet d’accéder aux relations de suivi de
    # utilisateurs qu’il suit.

    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by'
    )
    # related_name='followed_by' : permet d’accéder aux utilisateurs 
    # qui suivent cet utilisateur

    def __str__(self):
        return f"{self.user.username} -> {self.followed_user.username}"

    class Meta:
        unique_together = ('user', 'followed_user')
        # Instruction Django qui impose une relation unique
