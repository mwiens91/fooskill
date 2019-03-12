"""Contains settings for the admin page."""

from django.contrib import admin
from .models import Player, Game


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("player1", "player2")
