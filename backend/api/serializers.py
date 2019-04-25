"""Contains serializers for models."""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
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
        fields = ["id", "name", "user"]


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

    winner = serializers.SlugRelatedField(
        queryset=Player.objects.all(), slug_field="name"
    )
    loser = serializers.SlugRelatedField(
        queryset=Player.objects.all(), slug_field="name"
    )
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
        ]

    def validate(self, attrs):
        """Call model's clean method."""
        attrs = super().validate(attrs)

        try:
            Game(**attrs).clean()
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return attrs
