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
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The user associated with the player.",
    )

    class Meta:
        """Model metadata."""

        # Order by name in ascending order
        ordering = ["name"]

    def __str__(self):
        """String representation of player."""
        return self.name


class Game(models.Model):
    """A model for a particular game."""

    player1 = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        related_name="player1",
        help_text="One of the players.",
    )
    player2 = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        related_name="player2",
        help_text="The other player.",
    )
    player1_score = models.PositiveSmallIntegerField(
        default=0, help_text="Player 1's score."
    )
    player2_score = models.PositiveSmallIntegerField(
        default=0, help_text="Player 2's score."
    )
    datetime_played = models.DateTimeField(
        default=timezone.now,
        help_text="The date and time when the game was played.",
    )
    submitted_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        help_text="The user which submitted the game.",
    )

    class Meta:
        """Model metadata."""

        # Order by most recently played
        ordering = ["-datetime_played"]

    def __str__(self):
        """String representation of player."""
        return "%s vs %s (%s-%s)" % (
            self.player1,
            self.player2,
            self.player1_score,
            self.player2_score,
        )
