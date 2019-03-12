"""Contains settings for the admin page."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Game, Player, User


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("player1", "player2")


# Register custom user model
admin.site.register(User, UserAdmin)
