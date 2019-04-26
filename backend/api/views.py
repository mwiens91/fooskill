"""Contains view(sets) for the API."""

from rest_framework import viewsets
from .models import Game, MatchupStatsNode, Player, PlayerStatsNode, User
from .serializers import (
    GameSerializer,
    MatchupStatsNodeSerializer,
    PlayerSerializer,
    PlayerStatsNodeSerializer,
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
    http_method_names = ["get", "post", "patch"]
    serializer_class = PlayerSerializer


class PlayerStatsNodeViewSet(viewsets.ModelViewSet):
    """A viewset for player stats nodes."""

    queryset = PlayerStatsNode.objects.all()
    http_method_names = ["get"]
    serializer_class = PlayerStatsNodeSerializer


class MatchupStatsNodeViewSet(viewsets.ModelViewSet):
    """A viewset for matchup stats nodes."""

    queryset = MatchupStatsNode.objects.all()
    http_method_names = ["get"]
    serializer_class = MatchupStatsNodeSerializer


class GameViewSet(viewsets.ModelViewSet):
    """A viewset for games."""

    queryset = Game.objects.all()
    http_method_names = ["get", "post"]
    serializer_class = GameSerializer

    def get_serializer(self, *args, **kwargs):
        """Inject the user into the serializer if logged in."""
        serializer = super().get_serializer(*args, **kwargs)

        if (
            hasattr(serializer, "fields")
            and self.request.user.is_authenticated
        ):
            serializer.fields[
                "submitted_by"
            ].initial = self.request.user.username

        return serializer
