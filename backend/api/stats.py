"""Contains functions for calculating player and matchup statistics."""

from . import models


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
        games = previous_node.games
        wins = previous_node.wins
        losses = previous_node.losses
        average_goals_per_game = previous_node.average_goals_per_game
        average_goals_against_per_game = (
            previous_node.average_goals_against_per_game
        )
    else:
        games = 0
        wins = 0
        losses = 0
        average_goals_per_game = 0
        average_goals_against_per_game = 0

    # Calculate new stats
    games += 1

    if game.winner == player:
        # Grab the scores
        player_score = game.winner_score
        opponent_score = game.loser_score

        wins += 1
    else:
        player_score = game.loser_score
        opponent_score = game.winner_score

        losses += 1

    average_goals_per_game = calculate_new_average(
        avg=average_goals_per_game, N=games - 1, new_val=player_score
    )
    average_goals_against_per_game = calculate_new_average(
        avg=average_goals_against_per_game, N=games - 1, new_val=opponent_score
    )

    win_rate = wins / games

    # Create the node
    models.PlayerStatsNode.objects.create(
        player=player,
        game=game,
        games=games,
        wins=wins,
        losses=losses,
        win_rate=win_rate,
        average_goals_per_game=average_goals_per_game,
        average_goals_against_per_game=average_goals_against_per_game,
    )


def create_matchup_stats_node(player1, player2, game, previous_node=None):
    """Create a stats node for a player.

    Args:
        player1: An instance of the Player model corresponding to the
            player whose perspective to take.
        player2: An instance of the Player model corresponding to the
            opponent player.
        game: An instance of the Game model corresponding to the game to
            adjust stats from.
        previous_node: An optional instance of the MatchupStatsNode
            model corresponding to the matchup's last stats node
            (between player 1 and 2—in that order—as provided).
    """
    # Grab previous stats (if they exist)
    if previous_node is not None:
        games = previous_node.games
        wins = previous_node.wins
        losses = previous_node.losses
        average_goals_per_game = previous_node.average_goals_per_game
        average_goals_against_per_game = (
            previous_node.average_goals_against_per_game
        )
    else:
        games = 0
        wins = 0
        losses = 0
        average_goals_per_game = 0
        average_goals_against_per_game = 0

    # Calculate new stats
    games += 1

    if game.winner == player1:
        # Grab the scores
        player_score = game.winner_score
        opponent_score = game.loser_score

        wins += 1
    else:
        player_score = game.loser_score
        opponent_score = game.winner_score

        losses += 1

    average_goals_per_game = calculate_new_average(
        avg=average_goals_per_game, N=games - 1, new_val=player_score
    )
    average_goals_against_per_game = calculate_new_average(
        avg=average_goals_against_per_game, N=games - 1, new_val=opponent_score
    )

    win_rate = wins / games

    # Create the node
    models.MatchupStatsNode.objects.create(
        player1=player1,
        player2=player2,
        game=game,
        games=games,
        wins=wins,
        losses=losses,
        win_rate=win_rate,
        average_goals_per_game=average_goals_per_game,
        average_goals_against_per_game=average_goals_against_per_game,
    )
