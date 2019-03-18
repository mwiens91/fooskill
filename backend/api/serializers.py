"""Contains serializers for models."""

from rest_framework import serializers
from .models import Game, Player, User


class UserReadOnlySerializer(serializers.ModelSerializer):
    """A serializer for a user."""

    class Meta:
        model = User
        fields = ["username", "date_joined", "last_login", "is_staff"]


class PlayerSerializer(serializers.ModelSerializer):
    """A serializer for a player."""

    user = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="username"
    )

    class Meta:
        model = Player
        fields = ["id", "name", "user"]


class GameSerializer(serializers.ModelSerializer):
    """A serializer for a game."""

    winner = serializers.SlugRelatedField(
        queryset=Player.objects.all(), slug_field="name"
    )
    loser = serializers.SlugRelatedField(
        queryset=Player.objects.all(), slug_field="name"
    )
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
