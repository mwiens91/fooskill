"""Contains serializers for models."""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers
from .models import (
    Game,
    MatchupStatsNode,
    Player,
    PlayerRatingNode,
    PlayerStatsNode,
    RatingPeriod,
    User,
)


class UserReadOnlySerializer(serializers.ModelSerializer):
    """A serializer for a user."""

    class Meta:
        model = User
        fields = ("username", "date_joined", "last_login", "is_staff")


class RatingPeriodSerializer(serializers.ModelSerializer):
    """A serializer for a rating period.

    This should be read-only.
    """

    class Meta:
        model = RatingPeriod
        fields = ("id", "start_datetime", "end_datetime")


class PlayerSerializer(serializers.ModelSerializer):
    """A serializer for a player."""

    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username",
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Player

        # Only show rating volatility if rating algorithm is Glicko-2
        if settings.RATING_ALGORITHM == "glicko":
            fields = (
                "id",
                "name",
                "user",
                "is_active",
                "ranking",
                "ranking_delta",
                "rating",
                "rating_deviation",
                "inactivity",
                "games",
                "wins",
                "losses",
                "win_rate",
                "average_goals_per_game",
                "average_goals_against_per_game",
            )
            read_only_fields = (
                "id",
                "is_active",
                "ranking",
                "ranking_delta",
                "rating",
                "rating_deviation",
                "inactivity",
                "games",
                "wins",
                "losses",
                "win_rate",
                "average_goals_per_game",
                "average_goals_against_per_game",
            )
        else:
            fields = (
                "id",
                "name",
                "user",
                "is_active",
                "ranking",
                "ranking_delta",
                "rating",
                "rating_deviation",
                "rating_volatility",
                "inactivity",
                "games",
                "wins",
                "losses",
                "win_rate",
                "average_goals_per_game",
                "average_goals_against_per_game",
            )
            read_only_fields = (
                "id",
                "is_active",
                "ranking",
                "ranking_delta",
                "rating",
                "rating_deviation",
                "rating_volatility",
                "inactivity",
                "games",
                "wins",
                "losses",
                "win_rate",
                "average_goals_per_game",
                "average_goals_against_per_game",
            )


class PlayerStatsNodeSerializer(serializers.ModelSerializer):
    """A serializer for a player stats node.

    This is meant to be read-only (stats nodes are handled exclusively
    by the backend).
    """

    # Need to specify this manually here since datetime is a property
    # and hence the default timezone settings don't automatically apply
    # to this
    datetime = serializers.DateTimeField(
        default=lambda: timezone.localtime().strftime(
            settings.REST_FRAMEWORK["DATETIME_FORMAT"]
        ),
        initial=lambda: timezone.localtime().strftime(
            settings.REST_FRAMEWORK["DATETIME_FORMAT"]
        ),
    )

    class Meta:
        model = PlayerStatsNode
        fields = (
            "id",
            "datetime",
            "player",
            "game",
            "games",
            "wins",
            "losses",
            "win_rate",
            "average_goals_per_game",
            "average_goals_against_per_game",
        )


class MatchupStatsNodeSerializer(serializers.ModelSerializer):
    """A serializer for a matchup stats node.

    This is meant to be read-only (stats nodes are handled exclusively
    by the backend).
    """

    # Need to specify this manually here since datetime is a property
    # and hence the default timezone settings don't automatically apply
    # to this
    datetime = serializers.DateTimeField(
        default=lambda: timezone.localtime().strftime(
            settings.REST_FRAMEWORK["DATETIME_FORMAT"]
        ),
        initial=lambda: timezone.localtime().strftime(
            settings.REST_FRAMEWORK["DATETIME_FORMAT"]
        ),
    )

    class Meta:
        model = MatchupStatsNode
        fields = (
            "id",
            "datetime",
            "player1",
            "player2",
            "game",
            "games",
            "wins",
            "losses",
            "win_rate",
            "average_goals_per_game",
            "average_goals_against_per_game",
        )


class PlayerRatingNodeSerializer(serializers.ModelSerializer):
    """A serializer for a player rating node.

    This is meant to be read-only.
    """

    class Meta:
        model = PlayerRatingNode

        # Only show rating volatility if rating algorithm is Glicko-2
        if settings.RATING_ALGORITHM == "glicko":
            fields = (
                "id",
                "player",
                "rating_period",
                "ranking",
                "ranking_delta",
                "rating",
                "rating_deviation",
                "inactivity",
            )
        else:
            fields = (
                "id",
                "player",
                "rating_period",
                "ranking",
                "ranking_delta",
                "rating",
                "rating_deviation",
                "rating_volatility",
                "inactivity",
            )


class GameSerializer(serializers.ModelSerializer):
    """A serializer for a game.

    Note that the user is automatically injected into the submitted_by
    field for post methods.
    """

    winner_score = serializers.IntegerField(min_value=0, initial=8)
    loser_score = serializers.IntegerField(min_value=0, initial=0)
    submitted_by = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="username"
    )

    class Meta:
        model = Game
        fields = (
            "id",
            "datetime_played",
            "winner",
            "loser",
            "winner_score",
            "loser_score",
            "submitted_by",
            "rating_period",
            "winner_player_stats_node",
            "loser_player_stats_node",
            "winner_matchup_stats_node",
            "loser_matchup_stats_node",
        )
        read_only_fields = (
            "id",
            "datetime_played",
            "rating_period",
            "winner_player_stats_node",
            "loser_player_stats_node",
            "winner_matchup_stats_node",
            "loser_matchup_stats_node",
        )

    def validate(self, attrs):
        """Call model's clean method."""
        attrs = super().validate(attrs)

        try:
            Game(**attrs).clean()
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return attrs
