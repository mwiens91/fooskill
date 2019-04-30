"""Contains settings for the admin page."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Game,
    MatchupStatsNode,
    Player,
    PlayerRatingNode,
    PlayerStatsNode,
    RatingPeriod,
    User,
)


@admin.register(RatingPeriod)
class RatingPeriodAdmin(admin.ModelAdmin):
    """Settings for RatingPeriod model on admin page."""

    list_display = ("id", "start_datetime", "end_datetime")


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Settings for Game model on admin page."""

    list_max_show_all = 10000
    list_per_page = 200

    list_display = (
        "id",
        "datetime_played",
        "winner",
        "loser",
        "winner_score",
        "loser_score",
        "rating_period",
    )


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """Settings for Player model on admin page."""

    list_display = (
        "id",
        "name",
        "user",
        "is_active",
        "rating",
        "rating_deviation",
        "rating_volatility",
        "inactivity",
        "games",
        "wins",
        "losses",
        "average_goals_per_game",
    )


@admin.register(PlayerStatsNode)
class PlayerStatsNodeAdmin(admin.ModelAdmin):
    """Settings for PlayerStatsNode model on admin page."""

    list_display = (
        "id",
        "player",
        "datetime",
        "games",
        "wins",
        "losses",
        "average_goals_per_game",
    )


@admin.register(PlayerRatingNode)
class PlayerRatingNodeAdmin(admin.ModelAdmin):
    """Settings for PlayerRatingNode model on admin page."""

    list_display = (
        "id",
        "player",
        "rating_period",
        "rating",
        "rating_deviation",
        "rating_volatility",
        "inactivity",
    )


@admin.register(MatchupStatsNode)
class MatchupStatsNodeAdmin(admin.ModelAdmin):
    """Settings for MatchupStatsNode model on admin page."""

    list_display = (
        "id",
        "player1",
        "player2",
        "datetime",
        "games",
        "wins",
        "losses",
        "average_goals_per_game",
    )


# Register custom user model
admin.site.register(User, UserAdmin)
