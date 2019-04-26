"""Helper functions."""

from django.db import connection
from .models import Game, MatchupStatsNode, PlayerStatsNode


def reprocess_all_games(reset_pk_counter=True):
    """Wipes all existing stats nodes and creates new stats nodes.

    Args:
        reset_pk_counter: An optional boolean specifying whether to
            reset to pk counter for stats nodes back to 1.
    """
    # Wipe existing nodes
    PlayerStatsNode.objects.all().delete()
    MatchupStatsNode.objects.all().delete()

    # Reset pk counter
    if reset_pk_counter:
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
