"""Contains models definitions."""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from . import stats


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
        """String representation of a player.

        Use the username of the player's user if there's a user linked;
        otherwise just use the player name.
        """
        if self.user:
            return self.user.username

        return self.name

    @property
    def wins(self):
        """Returns the players win count."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.wins

    @property
    def losses(self):
        """Returns the players losses count."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.losses

    @property
    def average_goals_per_game(self):
        """Returns the players average goals per game."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.average_goals_per_game

    def get_all_player_stats_nodes(self):
        """Returns all of the player's stats nodes."""
        return PlayerStatsNode.objects.filter(player=self)

    def get_latest_player_stats_node(self):
        """Returns the player's latest stats node.

        Returns None if no stats nodes exist for the plyaer.
        """
        nodes = self.get_all_player_stats_nodes()

        if nodes:
            return nodes.first()

        return None


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
        node_queryset = self.playerstatsnode_set.filter(player=self.winner)

        if node_queryset:
            return node_queryset.first().pk

        return None

    @property
    def loser_stats_node(self):
        """Return the player stats node for the loser."""
        node_queryset = self.playerstatsnode_set.filter(player=self.loser)

        if node_queryset:
            return node_queryset.first().pk

        return None

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

    def process_game(self):
        """Process a game (e.g., update player stats)."""
        # Create winner and loser stats nodes
        if self.winner_stats_node is None:
            stats.create_player_stats_node(
                player=self.winner,
                game=self,
                previous_node=self.winner.get_latest_player_stats_node(),
            )

        if self.loser_stats_node is None:
            stats.create_player_stats_node(
                player=self.loser,
                game=self,
                previous_node=self.loser.get_latest_player_stats_node(),
            )


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

    class Meta:
        """Model metadata."""

        # Order by creation date (in order from most recent to oldest)
        ordering = ["-pk"]

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
