"""Contains models definitions."""

from django.db import models
from django.db.models.functions import Upper
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone


class User(AbstractUser):
    """Custom user model."""

    class Meta:
        """Model metadata."""

        # Order by username in ascending order
        ordering = [Upper("username")]


class Player(models.Model):
    """A model of a player and their stats."""

    name = models.CharField(
        max_length=200, unique=True, help_text="The player's name."
    )
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The user associated with the player.",
    )

    class Meta:
        """Model metadata."""

        # Order by name in ascending order
        ordering = [Upper("name")]

    def __str__(self):
        """String representation of player."""
        return self.name


class Game(models.Model):
    """A model for a particular game."""

    winner = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        related_name="winner",
        help_text="The game's winner.",
    )
    loser = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        related_name="loser",
        help_text="The game's loser.",
    )
    winner_score = models.PositiveSmallIntegerField(
        default=8, help_text="The winner's score."
    )
    loser_score = models.PositiveSmallIntegerField(
        default=0, help_text="The loser's score."
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

    def clean(self):
        """Perform basic validation."""
        # Make sure the winner's score is greater than the loser's
        if not self.winner_score > self.loser_score:
            raise ValidationError(
                "Winner score must be greater than loser score!"
            )

        # Make sure the two players are distinct
        if self.winner == self.loser:
            raise ValidationError("Winner and loser must be distinct!")

    def __str__(self):
        """String representation of player."""
        return "%s vs %s (%s-%s)" % (
            self.winner,
            self.loser,
            self.winner_score,
            self.loser_score,
        )
