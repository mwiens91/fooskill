"""Contains serializers for models."""

from django.conf import settings
from django.utils import timezone
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
        queryset=User.objects.all(),
        slug_field="username",
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Player
        fields = ["id", "name", "user"]


class GameSerializer(serializers.ModelSerializer):
    """A serializer for a game."""

    datetime_played = serializers.DateTimeField(
        default=lambda: timezone.now().strftime(
            settings.REST_FRAMEWORK["DATETIME_FORMAT"]
        ),
        initial=lambda: timezone.now().strftime(
            settings.REST_FRAMEWORK["DATETIME_FORMAT"]
        ),
    )
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
