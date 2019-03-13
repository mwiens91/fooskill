"""Contains view(sets) for the API."""

from rest_framework import viewsets
from .models import Game, Player, User
from .serializers import GameSerializer, PlayerSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """A viewset for users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    """A viewset for players."""

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class GameViewSet(viewsets.ModelViewSet):
    """A viewset for games."""

    queryset = Game.objects.all()
    serializer_class = GameSerializer
