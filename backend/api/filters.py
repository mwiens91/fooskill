"""Contains filtersets for REST API viewsets."""

from django_filters import rest_framework as filters
from .models import (
    Game,
    MatchupStatsNode,
    Player,
    PlayerRatingNode,
    PlayerStatsNode,
    RatingPeriod,
    User,
)


# Common lookups for filter fields
ID_FIELD_LOOKUPS = ["exact"]
CHAR_FIELD_LOOKUPS = [
    "exact",
    "contains",
    "in",
    "startswith",
    "endswith",
    "regex",
]
NUM_FIELD_LOOKUPS = ["exact", "in", "range", "lt", "lte", "gt", "gte"]
BOOLEAN_FIELD_LOOKUPS = ["exact"]
FOREIGN_KEY_FIELD_LOOKUPS = ["exact", "in"]
DATE_FIELD_LOOKUPS = ["exact", "in", "range", "lt", "lte", "gt", "gte"]


class UserFilter(filters.FilterSet):
    """A filterset to support queries for Users."""

    class Meta:
        model = User
        fields = {"is_staff": BOOLEAN_FIELD_LOOKUPS}


class RatingPeriodFilter(filters.FilterSet):
    """A filterset to support queries for RatingPeriods."""

    class Meta:
        model = RatingPeriod
        fields = {
            "id": NUM_FIELD_LOOKUPS,
            "start_datetime": DATE_FIELD_LOOKUPS,
            "end_datetime": DATE_FIELD_LOOKUPS,
        }


class PlayerFilter(filters.FilterSet):
    """A filterset to support queries for Players."""

    class Meta:
        model = Player
        fields = {
            "id": ID_FIELD_LOOKUPS,
            "name": CHAR_FIELD_LOOKUPS,
            "user": FOREIGN_KEY_FIELD_LOOKUPS,
        }


class PlayerStatsNodeFilter(filters.FilterSet):
    """A filterset to support queries for PlayerStatsNodes."""

    class Meta:
        model = PlayerStatsNode
        fields = {
            "id": ID_FIELD_LOOKUPS,
            "player": FOREIGN_KEY_FIELD_LOOKUPS,
            "game": FOREIGN_KEY_FIELD_LOOKUPS,
        }


class MatchupStatsNodeFilter(filters.FilterSet):
    """A filterset to support queries for MatchupStatsNodes."""

    class Meta:
        model = MatchupStatsNode
        fields = {
            "id": ID_FIELD_LOOKUPS,
            "player1": FOREIGN_KEY_FIELD_LOOKUPS,
            "player2": FOREIGN_KEY_FIELD_LOOKUPS,
            "game": FOREIGN_KEY_FIELD_LOOKUPS,
        }


class GameFilter(filters.FilterSet):
    """A filterset to support queries for Games."""

    class Meta:
        model = Game
        fields = {
            "id": ID_FIELD_LOOKUPS,
            "datetime_played": DATE_FIELD_LOOKUPS,
            "winner": FOREIGN_KEY_FIELD_LOOKUPS,
            "loser": FOREIGN_KEY_FIELD_LOOKUPS,
            "winner_score": NUM_FIELD_LOOKUPS,
            "loser_score": NUM_FIELD_LOOKUPS,
            "submitted_by": FOREIGN_KEY_FIELD_LOOKUPS,
            "rating_period": FOREIGN_KEY_FIELD_LOOKUPS,
        }
