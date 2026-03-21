from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from typing import TYPE_CHECKING


class UserFollow(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by'
    )

    def __str__(self):
        return f"{self.user.username} -> {self.followed_user.username}"

    class Meta:
        unique_together = ('user', 'followed_user')
