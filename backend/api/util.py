"""Helper functions."""

from datetime import timedelta
from django.conf import settings
from django.db import connection
from django.utils import timezone
from .models import Game, MatchupStatsNode, PlayerStatsNode, RatingPeriod
from .ratings import calculate_new_rating_period


def reprocess_all_stats(reset_id_counter=True):
    """Wipes all existing stats nodes and creates new stats nodes.

    Args:
        reset_id_counter: An optional boolean specifying whether to
            reset to ID counter for stats nodes back to 1.
    """
    # Wipe existing nodes
    PlayerStatsNode.objects.all().delete()
    MatchupStatsNode.objects.all().delete()

    # Reset ID counter
    if reset_id_counter:
        with connection.cursor() as cursor:
            cursor.execute(
                "ALTER SEQUENCE api_playerstatsnode_id_seq RESTART with 1"
            )
            cursor.execute(
                "ALTER SEQUENCE api_matchupstatsnode_id_seq RESTART with 1"
            )

    # Recreate nodes
    for game in Game.objects.order_by("datetime_played"):
        game.process_game()


def process_new_ratings():
    """Calculates any new potential rating periods."""
    # Find first datetime where there exists unrated games. Recall that
    # rating periods and games are ordered from newest to oldest.
    latest_rating_period = RatingPeriod.objects.first()

    if latest_rating_period:
        start_datetime = (
            latest_rating_period.end_datetime + timedelta.resolution
        )
    else:
        # No rating periods. Use the date of the earliest game if one
        # exists; if no games exist, return.
        earliest_game = Game.objects.last()

        if not earliest_game:
            return

        start_datetime = earliest_game.datetime_played

    # Find out whether there's been enough time elapsed to make a new
    # rating period
    end_datetime = start_datetime + timedelta(
        days=settings.GLICKO2_RATING_PERIOD_DAYS
    )

    # Not enough time elapsed: return.
    if end_datetime > timezone.now():
        return

    # Calculate the new rating period and call this function again
    calculate_new_rating_period(start_datetime, end_datetime)

    # Go again
    process_new_ratings()


def reprocess_all_ratings(reset_id_counter=True):
    """Wipes existing rating periods and rating nodes and creates new ones.

    Args:
        reset_id_counter: An optional boolean specifying whether to
            reset to ID counter for stats nodes back to 1.
    """
    # Wipe all existing rating periods and rating nodes. Note that
    # manually deleting player rating nodes isn't strictly neccessary,
    # since they should all be deleted when their corresponding rating
    # periods are deleted.
    RatingPeriod.objects.all().delete()

    # Reset ID counter
    if reset_id_counter:
        with connection.cursor() as cursor:
            cursor.execute(
                "ALTER SEQUENCE api_playerratingsnode_id_seq RESTART with 1"
            )
            cursor.execute(
                "ALTER SEQUENCE api_ratingperiod_id_seq RESTART with 1"
            )

    # Recalculate ratings
    process_new_ratings()
