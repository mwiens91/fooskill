"""Contains models definitions."""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Custom user model."""

    pass


class Player(models.Model):
    """A model of a player and their stats."""
    name = models.CharField(
        max_length=200, unique=True, help_text="The player's name."
    )


class Game(models.Model):
    """A model for a particular game."""
    player1 = models.ForeignKey(
        Player, on_delete=models.PROTECT, related_name="player1"
    )
    player2 = models.ForeignKey(
        Player, on_delete=models.PROTECT, related_name="player2"
    )
    player1_score = models.PositiveSmallIntegerField(default=0)
    player2_score = models.PositiveSmallIntegerField(default=0)
    datetime_played = models.DateTimeField(default=timezone.now)
