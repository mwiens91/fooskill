"""Contains serializers for models."""

from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Game, Player, PlayerStatsNode, User


class UserReadOnlySerializer(serializers.ModelSerializer):
    """A serializer for a user."""

    class Meta:
        model = User
        fields = ["username", "date_joined", "last_login", "is_staff"]


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
        fields = [
            "id",
            "name",
            "user",
            "wins",
            "losses",
            "average_goals_per_game",
        ]


class PlayerStatsNodeSerializer(serializers.ModelSerializer):
    """A serializer for a player stats node."""

    class Meta:
        model = PlayerStatsNode
        fields = [
            "datetime",
            "player",
            "game",
            "wins",
            "losses",
            "average_goals_per_game",
        ]


class GameSerializer(serializers.ModelSerializer):
    """A serializer for a game."""

    winner_score = serializers.IntegerField(min_value=0, initial=8)
    loser_score = serializers.IntegerField(min_value=0, initial=0)
    submitted_by = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="username"
    )

    class Meta:
        model = Game
        fields = [
            "id",
            "datetime_played",
            "winner",
            "loser",
            "winner_score",
            "loser_score",
            "submitted_by",
            "winner_stats_node",
            "loser_stats_node",
        ]

    def validate(self, attrs):
        """Call model's clean method."""
        attrs = super().validate(attrs)

        try:
            Game(**attrs).clean()
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return attrs
