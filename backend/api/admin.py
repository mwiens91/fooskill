"""Contains settings for the admin page."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Game, MatchupStatsNode, Player, PlayerStatsNode, User


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Settings for Game model on admin page."""

    list_max_show_all = 10000
    list_per_page = 200

    list_display = (
        "datetime_played",
        "winner",
        "loser",
        "winner_score",
        "loser_score",
    )


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """Settings for Player model on admin page."""

    list_display = (
        "name",
        "user",
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
