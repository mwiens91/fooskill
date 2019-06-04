"""Contains functions for calculating player and matchup statistics."""

from . import models


def calculate_new_average(avg, N, new_val):
    """Calculate new average given a new value and an existing average.

    Args:
        avg: The old average value.
        N: The old number of data points averaged over.
        new_val: The new value to recalculate the average with.

    Returns:
        The new average value.
    """
    return (avg * N + new_val) / (N + 1)


def calculate_new_common_stats(
    old_games,
    old_wins,
    old_losses,
    old_average_goals_per_game,
    old_average_goals_against_per_game,
    player_is_winner,
    player_score,
    opponent_score,
):
    """Calculate new common stats for a player.

    This can be done in the context of all games or a particular
    matchup.

    Args:
        old_games: The number of games previously played by the player.
        old_wins: The number of games won previously by the player.
        old_losses: The number of games lost previously by the player.
        old_average_goals_per_game: The previous average goals per game
            the player scored.
        old_average_goals_against_per_game: The previous average goals
            per game the opponent(s) scored.
        player_is_winner: A boolean indicating whether the player won
            the game.
        player_score: The number of goals the player scored for the game
            under consideration.
        opponent_score: The number of goals the opponent scored for the
            game under consideration.

    Returns:
        A dictionary containing the new number of games, wins, losses,
        average goals per game, average goals against per game, and win
        rate.
    """
    # Calculate new stats
    games = old_games + 1

    if player_is_winner:
        wins = old_wins + 1
        losses = old_losses
    else:
        wins = old_wins
        losses = old_losses + 1

    average_goals_per_game = calculate_new_average(
        avg=old_average_goals_per_game, N=old_games, new_val=player_score
    )
    average_goals_against_per_game = calculate_new_average(
        avg=old_average_goals_against_per_game,
        N=old_games,
        new_val=opponent_score,
    )

    win_rate = wins / games

    return dict(
        games=games,
        wins=wins,
        losses=losses,
        average_goals_per_game=average_goals_per_game,
        average_goals_against_per_game=average_goals_against_per_game,
        win_rate=win_rate,
    )


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

    if game.winner == player:
        player_score = game.winner_score
        opponent_score = game.loser_score
    else:
        player_score = game.loser_score
        opponent_score = game.winner_score

    # Create the node
    models.PlayerStatsNode.objects.create(
        player=player,
        game=game,
        **calculate_new_common_stats(
            old_games=games,
            old_wins=wins,
            old_losses=losses,
            old_average_goals_per_game=average_goals_per_game,
            old_average_goals_against_per_game=average_goals_against_per_game,
            player_is_winner=game.winner == player,
            player_score=player_score,
            opponent_score=opponent_score,
        ),
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

    if game.winner == player1:
        player_score = game.winner_score
        opponent_score = game.loser_score
    else:
        player_score = game.loser_score
        opponent_score = game.winner_score

    # Create the node
    models.MatchupStatsNode.objects.create(
        player1=player1,
        player2=player2,
        game=game,
        **calculate_new_common_stats(
            old_games=games,
            old_wins=wins,
            old_losses=losses,
            old_average_goals_per_game=average_goals_per_game,
            old_average_goals_against_per_game=average_goals_against_per_game,
            player_is_winner=game.winner == player1,
            player_score=player_score,
            opponent_score=opponent_score,
        ),
    )
