"""Contains models definitions."""

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from . import stats


class User(AbstractUser):
    """Custom user model."""

    class Meta:
        """Model metadata."""

        # Order by username in ascending order
        ordering = ["username"]


class RatingPeriod(models.Model):
    """A model for a Glicko rating period."""

    start_datetime = models.DateTimeField(
        help_text="The starting datetime for the rating period."
    )
    end_datetime = models.DateTimeField(
        help_text="The starting datetime for the rating period."
    )

    class Meta:
        """Model metadata."""

        # Order by creation date (in order from most recent to oldest)
        ordering = ["-end_datetime"]

    def __str__(self):
        """String representation of a rating period."""
        return str(self.id)


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
        ordering = ["name", "id"]

    def __str__(self):
        """String representation of a player."""
        return "%s #%04d" % (self.name, self.id)

    @property
    def ranking(self):
        """Returns the players ranking."""
        node = self.get_latest_player_rating_node()

        if node is None:
            return None

        return node.ranking

    @property
    def ranking_delta(self):
        """Returns the players ranking change."""
        node = self.get_latest_player_rating_node()

        if node is None:
            return None

        return node.ranking_delta

    @property
    def rating(self):
        """Returns the players rating."""
        node = self.get_latest_player_rating_node()

        if node is None:
            if settings.RATING_ALGORITHM == "glicko":
                return settings.GLICKO_BASE_RATING

            return settings.GLICKO2_BASE_RATING

        return node.rating

    @property
    def rating_deviation(self):
        """Returns the players rating deviation."""
        node = self.get_latest_player_rating_node()

        if node is None:
            if settings.RATING_ALGORITHM == "glicko":
                return settings.GLICKO_BASE_RD

            return settings.GLICKO2_BASE_RD

        return node.rating_deviation

    @property
    def rating_volatility(self):
        """Returns the players rating volatility.

        This parameter is only relevant if the rating algorithm is
        Glicko-2 and will always be None if the rating algorithm is
        Glicko (cf. Glicko-2).
        """
        # Get out if rating algorithm is Glicko
        if settings.RATING_ALGORITHM == "glicko":
            return None

        # Rating algorithm is Glicko-2
        node = self.get_latest_player_rating_node()

        if node is None:
            return settings.GLICKO2_BASE_VOLATILITY

        return node.rating_volatility

    @property
    def inactivity(self):
        """Returns the players rating period inactivity."""
        node = self.get_latest_player_rating_node()

        if node is None:
            return 0

        return node.inactivity

    @property
    def is_active(self):
        """Returns whether the player is active."""
        node = self.get_latest_player_rating_node()

        if node is None:
            return False

        return node.is_active

    @property
    def games(self):
        """Returns the players game count."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.games

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
    def win_rate(self):
        """Returns the players win rate."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.win_rate

    @property
    def average_goals_per_game(self):
        """Returns the players average goals per game."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.average_goals_per_game

    @property
    def average_goals_against_per_game(self):
        """Returns the players average goals against per game."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.average_goals_against_per_game

    def get_all_player_stats_nodes(self):
        """Returns all of the player's stats nodes."""
        return PlayerStatsNode.objects.filter(player=self)

    def get_latest_player_stats_node(self):
        """Returns the player's latest stats node.

        Returns None if no stats nodes exist for the player.
        """
        nodes = self.get_all_player_stats_nodes()

        if nodes:
            return nodes.first()

        return None

    def get_all_matchup_stats_nodes(self, opponent):
        """Returns all of the player's matchup stats nodes against an opponent.

        Args:
            opponent: A Player model instance to filter against. If this
                isn't provided, matchup nodes will be returned for all
                opponents.
        """
        return MatchupStatsNode.objects.filter(player1=self, player2=opponent)

    def get_latest_matchup_stats_node(self, opponent):
        """Returns the player's latest matchup stats node against an opponent.

        Args:
            opponent: A Player model instance to filter against. If this
                isn't provided, matchup nodes will be returned for all
                opponents.
        """
        nodes = self.get_all_matchup_stats_nodes(opponent)

        if nodes:
            return nodes.first()

        return None

    def get_all_player_rating_nodes(self):
        """Returns all of the player's rating nodes."""
        return PlayerRatingNode.objects.filter(player=self)

    def get_latest_player_rating_node(self):
        """Returns the player's latest rating node.

        Returns None if no rating nodes exist for the player.
        """
        nodes = self.get_all_player_rating_nodes()

        if nodes:
            return nodes.first()

        return None

    def get_first_game_played(self):
        """Returns the first game played by the player.

        Returns None if the player has not played games.
        """
        games_played = Game.objects.filter(Q(winner=self) | Q(loser=self))

        if not games_played:
            return None

        return games_played.last()


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
    rating_period = models.ForeignKey(
        RatingPeriod,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The rating period this game is apart of",
    )

    class Meta:
        """Model metadata."""

        # Order by most recently played
        ordering = ["-datetime_played"]

    def __str__(self):
        """String representation of a game."""
        return str(self.id)

    @property
    def winner_player_stats_node(self):
        """Return the player stats node for the winner."""
        node_queryset = self.playerstatsnode_set.filter(
            player=self.winner, game=self
        )

        if node_queryset:
            return node_queryset.first().id

        return None

    @property
    def loser_player_stats_node(self):
        """Return the player stats node for the loser."""
        node_queryset = self.playerstatsnode_set.filter(
            player=self.loser, game=self
        )

        if node_queryset:
            return node_queryset.first().id

        return None

    @property
    def winner_matchup_stats_node(self):
        """Return the matchup stats node for the winner."""
        node_queryset = self.matchupstatsnode_set.filter(
            player1=self.winner, player2=self.loser, game=self
        )

        if node_queryset:
            return node_queryset.first().id

        return None

    @property
    def loser_matchup_stats_node(self):
        """Return the matchup stats node for the loser."""
        node_queryset = self.matchupstatsnode_set.filter(
            player1=self.loser, player2=self.winner, game=self
        )

        if node_queryset:
            return node_queryset.first().id

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
        """Update player and matchup stats based on game results."""
        # Create stats nodes
        if self.winner_player_stats_node is None:
            stats.create_player_stats_node(
                player=self.winner,
                game=self,
                previous_node=self.winner.get_latest_player_stats_node(),
            )

        if self.loser_player_stats_node is None:
            stats.create_player_stats_node(
                player=self.loser,
                game=self,
                previous_node=self.loser.get_latest_player_stats_node(),
            )

        if self.winner_matchup_stats_node is None:
            stats.create_matchup_stats_node(
                player1=self.winner,
                player2=self.loser,
                game=self,
                previous_node=self.winner.get_latest_matchup_stats_node(
                    self.loser
                ),
            )

        if self.loser_matchup_stats_node is None:
            stats.create_matchup_stats_node(
                player1=self.loser,
                player2=self.winner,
                game=self,
                previous_node=self.loser.get_latest_matchup_stats_node(
                    self.winner
                ),
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
        help_text="The game which updated the player's stats.",
    )
    games = models.PositiveIntegerField(
        help_text="The number of games a player has played."
    )
    wins = models.PositiveIntegerField(
        help_text="The number of wins the player has."
    )
    losses = models.PositiveIntegerField(
        help_text="The number of losses the player has."
    )
    win_rate = models.FloatField(help_text="The player's win rate.")
    average_goals_per_game = models.FloatField(
        help_text="The average number of goals scored per game by the player."
    )
    average_goals_against_per_game = models.FloatField(
        help_text="The average number of goals scored against the player per game."
    )

    class Meta:
        """Model metadata."""

        # Order by creation date (in order from most recent to oldest)
        ordering = ["-id"]

    def __str__(self):
        """String representation of a player stats node."""
        return "%s (game ID: %s; date: %s)" % (
            self.player,
            self.game.id,
            self.datetime,
        )

    @property
    def datetime(self):
        """Returns the date of the node's game."""
        return self.game.datetime_played


class MatchupStatsNode(models.Model):
    """A player matchup's stats snapshot at a particular point in time

    Two matchup nodes will be generated for each game played by a given
    matchup, each from the perspective of one of the players.
    """

    player1 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="player1",
        help_text="The player in the matchup whose perspective to take.",
    )
    player2 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="player2",
        help_text='The "opponent" player in the matchup.',
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        help_text="The game which updated the matchup's stats.",
    )
    games = models.PositiveIntegerField(
        help_text="The number of games played by the matchup."
    )
    wins = models.PositiveIntegerField(
        help_text="The number of wins the player1 has."
    )
    losses = models.PositiveIntegerField(
        help_text="The number of losses the player1 has."
    )
    win_rate = models.FloatField(
        help_text="player1's win rate against player2."
    )
    average_goals_per_game = models.FloatField(
        help_text="The average number of goals scored per game by player1."
    )
    average_goals_against_per_game = models.FloatField(
        help_text="The average number of goals scored per game by player2."
    )

    class Meta:
        """Model metadata."""

        # Order by creation date (in order from most recent to oldest)
        ordering = ["-id"]

    def __str__(self):
        """String representation of a matchup stats node."""
        return "%s vs %s (game ID: %s; date: %s)" % (
            self.player1,
            self.player2,
            self.game.id,
            self.datetime,
        )

    @property
    def datetime(self):
        """Returns the date of the node's game."""
        return self.game.datetime_played


class PlayerRatingNode(models.Model):
    """A player's rating for a given rating period."""

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        help_text="The player corresponding whose ratings this node is for.",
    )
    rating_period = models.ForeignKey(
        RatingPeriod,
        on_delete=models.CASCADE,
        help_text="The rating period this rating was calculated in.",
    )
    ranking = models.PositiveSmallIntegerField(
        null=True, help_text="The player's rating for this rating period."
    )
    ranking_delta = models.SmallIntegerField(
        null=True,
        help_text="The player's rating change for this rating period.",
    )
    rating = models.FloatField(
        help_text="The player's rating for this rating period."
    )
    rating_deviation = models.FloatField(
        help_text="The player's rating deviation for this rating period."
    )
    rating_volatility = models.FloatField(
        null=True,
        help_text="The player's rating volatility for this rating period. This is only used if the rating algorithm is Glicko-2.",
    )
    inactivity = models.PositiveSmallIntegerField(
        help_text="How many rating periods the player has been inactive for."
    )
    is_active = models.BooleanField(
        help_text="Whether the player was considered active during this rating period."
    )

    class Meta:
        """Model metadata."""

        # Order by creation date (in order from most recent to oldest)
        ordering = ["-id"]

    def __str__(self):
        """String representation of a player rating node.

        Only shows rating volatility if the rating algorithm is
        Glicko-2.
        """
        if settings.RATING_ALGORITHM == "glicko":
            return "%s RP=%s r=%d, RD=%d" % (
                self.player,
                self.rating_period.id,
                self.rating,
                self.rating_deviation,
            )

        return "%s RP=%s r=%d, RD=%d, σ=%.2f" % (
            self.player,
            self.rating_period.id,
            self.rating,
            self.rating_deviation,
            self.rating_volatility,
        )


@receiver(post_save, sender=Game)
def process_game_hook(instance, created, **_):
    """Process a game immediately after game creation."""
    if created:
        instance.process_game()


@receiver(post_save, sender=User)
def create_auth_token(instance, created, **_):
    """Create an auth token for each new user."""
    if created:
        Token.objects.create(user=instance)
