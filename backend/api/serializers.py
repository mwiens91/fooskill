"""Contains serializers for models."""

from rest_framework import serializers
from .models import Game, Player, User


class UserSerializer(serializers.ModelSerializer):
    """A serializer for a user."""

    class Meta:
        model = User
        fields = ["username", "date_joined", "last_login", "is_staff"]


class PlayerSerializer(serializers.ModelSerializer):
    """A serializer for a player."""

    class Meta:
        model = Player
        fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
    """A serializer for a game."""

    class Meta:
        model = Game
        fields = "__all__"
