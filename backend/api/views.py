"""Contains view(sets) for the API."""

from rest_framework import viewsets
from .models import Game, Player, User
from .serializers import (
    GameSerializer,
    PlayerSerializer,
    UserReadOnlySerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """A viewset for users."""

    queryset = User.objects.all()
    lookup_field = "username"
    http_method_names = ["get"]
    serializer_class = UserReadOnlySerializer


class PlayerViewSet(viewsets.ModelViewSet):
    """A viewset for players."""

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class GameViewSet(viewsets.ModelViewSet):
    """A viewset for games."""

    queryset = Game.objects.all()
    serializer_class = GameSerializer
