"""Contains functions for calculating statistics and ratings."""

from .models import PlayerStatsNode


def calculate_new_average(avg, N, new_val):
    """Calculate new average given a new value and an existing average.

    Args:
        avg: The old average value.
        N: The old number of data points averaged over.
        new_val: The new value to recalculate the average with.
    """
    return (avg * N + new_val) / (N + 1)


def create_player_stats_node(player, game, previous_node=None):
    """Create a stats node for a player.

    Args:
        player: An instance of the Player model corresponding to the
            player.
        game: An instance of the Game model corresponding to the game to
            adjust stats from.
        previous_node: An optional instance of the PlayerStatsNode model
            corresponding to the player's last stats node.
    """
    # Grab previous stats (if they exist)
    if previous_node is not None:
        wins = previous_node.wins
        losses = previous_node.losses
        average_goals_per_game = previous_node.average_goals_per_game
    else:
        wins = 0
        losses = 0
        average_goals_per_game = 0

    # Calculate new stats
    if game.winner == player:
        # Grab the score
        score = game.winner_score

        wins += 1
    else:
        score = game.loser_score

        losses += 1

    average_goals_per_game = calculate_new_average(
        avg=average_goals_per_game, N=wins + losses - 1, new_val=score
    )

    # Create the node
    PlayerStatsNode.objects.create(
        player=player,
        game=game,
        wins=wins,
        losses=losses,
        average_goals_per_game=average_goals_per_game,
    )
