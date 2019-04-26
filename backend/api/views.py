"""Contains view(sets) for the API."""

from rest_framework import viewsets
from .filters import (
    GameFilter,
    MatchupStatsNodeFilter,
    PlayerFilter,
    PlayerStatsNodeFilter,
    RatingPeriodFilter,
    UserFilter,
)
from .models import (
    Game,
    MatchupStatsNode,
    Player,
    PlayerRatingNode,
    PlayerStatsNode,
    RatingPeriod,
    User,
)
from .serializers import (
    GameSerializer,
    MatchupStatsNodeSerializer,
    PlayerSerializer,
    PlayerStatsNodeSerializer,
    RatingPeriodSerializer,
    UserReadOnlySerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """A viewset for users."""

    queryset = User.objects.all()
    lookup_field = "username"
    http_method_names = ["get"]
    serializer_class = UserReadOnlySerializer
    filter_class = UserFilter


class RatingPeriodViewSet(viewsets.ModelViewSet):
    """A viewset for rating periods."""

    queryset = RatingPeriod.objects.all()
    http_method_names = ["get"]
    serializer_class = RatingPeriodSerializer
    filter_class = RatingPeriodFilter


class PlayerViewSet(viewsets.ModelViewSet):
    """A viewset for players."""

    queryset = Player.objects.all()
    http_method_names = ["get", "post", "patch"]
    serializer_class = PlayerSerializer
    filter_class = PlayerFilter


class PlayerStatsNodeViewSet(viewsets.ModelViewSet):
    """A viewset for player stats nodes."""

    queryset = PlayerStatsNode.objects.all()
    http_method_names = ["get"]
    serializer_class = PlayerStatsNodeSerializer
    filter_class = PlayerStatsNodeFilter


class MatchupStatsNodeViewSet(viewsets.ModelViewSet):
    """A viewset for matchup stats nodes."""

    queryset = MatchupStatsNode.objects.all()
    http_method_names = ["get"]
    serializer_class = MatchupStatsNodeSerializer
    filter_class = MatchupStatsNodeFilter


class GameViewSet(viewsets.ModelViewSet):
    """A viewset for games."""

    queryset = Game.objects.all()
    http_method_names = ["get", "post"]
    serializer_class = GameSerializer
    filter_class = GameFilter

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
