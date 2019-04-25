"""Contains models definitions."""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone


class User(AbstractUser):
    """Custom user model."""

    class Meta:
        """Model metadata."""

        # Order by username in ascending order
        ordering = ["username"]


class Player(models.Model):
    """A model of a player and their stats."""

    name = models.CharField(
        max_length=200, unique=True, help_text="The player's name."
    )
    user = models.OneToOneField(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The user associated with the player.",
    )

    class Meta:
        """Model metadata."""

        # Order by name in ascending order
        ordering = ["name"]

    def __str__(self):
        """String representation of a player."""
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
        auto_now_add=True,
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
        """String representation of a game."""
        return "%s vs %s (%s-%s)" % (
            self.winner,
            self.loser,
            self.winner_score,
            self.loser_score,
        )

    @property
    def winner_stats_node(self):
        """Return the player stats node for the winner."""
        nodes = self.playerstatsnode_set

        for node in nodes:
            if node.player == self.winner:
                return node

    @property
    def loser_stats_node(self):
        """Return the player stats node for the loser."""
        nodes = self.playerstatsnode_set

        for node in nodes:
            if node.player == self.loser:
                return node

    def clean(self):
        """Perform basic validation."""
        # Make sure the winner's score is greater than the loser's
        if self.winner_score <= self.loser_score:
            raise ValidationError(
                "Winner score must be greater than loser score!"
            )

        # Make sure the two players are distinct
        if self.winner == self.loser:
            raise ValidationError("Winner and loser must be distinct!")


class PlayerStatsNode(models.Model):
    """A player's stats snapshot at a particular point in time

    A node will be generated for each game played by a player.
    """

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        help_text="The player to record stats for.",
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        help_text="The latest game which updated the player's stats.",
    )
    wins = models.PositiveIntegerField(
        help_text="The number of wins the player has"
    )
    losses = models.PositiveIntegerField(
        help_text="The number of losses the player has"
    )
    average_goals_per_game = models.FloatField(
        help_text="The average number of goals scored per game by the player"
    )

    def __str__(self):
        """String repesentation of a player stats node."""
        return "%s (linked game: %s; date: %s)" % (
            self.player.name,
            self.game.pk,
            self.datetime,
        )

    @property
    def datetime(self):
        """Returns the date of the node's game."""
        return self.game.datetime_played
