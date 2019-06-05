"""Contains functions for calculating player ratings."""

from django.conf import settings
from . import models
from . import glicko
from . import glicko2

# The rating algorithm to use
RATING_ALGORITHM = settings.RATING_ALGORITHM


def calculate_new_rating_period(start_datetime, end_datetime):
    """Calculate a new ratings and a corresponding new rating period.

    Args:
        start_datetime: The datetime for the start of the rating period.
        end_datetime: The datetime for the end of the rating period.
    """
    # Create the rating period
    rating_period = models.RatingPeriod.objects.create(
        start_datetime=start_datetime, end_datetime=end_datetime
    )

    # Grab all games that will be in this rating period
    games = models.Game.objects.filter(
        datetime_played__gte=start_datetime, datetime_played__lte=end_datetime
    )

    # Mark all of the above games as belonging in this rating period
    for game in games:
        game.rating_period = rating_period
        game.save()

    # For each player, find all their matches, their scores in those
    # matches; then calculate their ratings. The new_ratings dictionary
    # contains players as keys, and dictionaries containing their new
    # rating parameters as the dictionary values.
    new_ratings = {}

    for player in models.Player.objects.all():
        # Don't calculate anything if they player's first game is prior
        # to this rating period
        first_game_played = player.get_first_game_played()

        if (
            first_game_played is None
            or first_game_played.datetime_played > end_datetime
        ):
            continue

        # Get the players rating parameters
        player_rating = player.rating
        player_rating_deviation = player.rating_deviation
        player_inactivity = player.inactivity

        if RATING_ALGORITHM == "glicko2":
            player_rating_volatility = player.rating_volatility

        # Build up the per-game rating parameters of opponents
        opponent_ratings = []
        opponent_rating_deviations = []
        scores = []

        for won_game in games.filter(winner=player):
            opponent_ratings.append(won_game.loser.rating)
            opponent_rating_deviations.append(won_game.loser.rating_deviation)
            scores.append(1)

        for lost_game in games.filter(loser=player):
            opponent_ratings.append(lost_game.winner.rating)
            opponent_rating_deviations.append(
                lost_game.winner.rating_deviation
            )
            scores.append(0)

        # Convert empty lists (meaning no matches) to None types
        if not opponent_ratings:
            opponent_ratings = None
            opponent_rating_deviations = None
            scores = None

        if RATING_ALGORITHM == "glicko":
            new_player_rating, new_player_rating_deviation, = glicko.calculate_player_rating(
                r=player_rating,
                RD=player_rating_deviation,
                opponent_rs=opponent_ratings,
                opponent_RDs=opponent_rating_deviations,
                scores=scores,
            )

            new_player_rating_volatility = None
        else:
            # Glicko-2
            new_player_rating, new_player_rating_deviation, new_player_rating_volatility = glicko2.calculate_player_rating(
                r=player_rating,
                RD=player_rating_deviation,
                sigma=player_rating_volatility,
                opponent_rs=opponent_ratings,
                opponent_RDs=opponent_rating_deviations,
                scores=scores,
            )

        # Calculate new inactivity
        if opponent_ratings is None:
            new_player_inactivity = player_inactivity + 1
        else:
            new_player_inactivity = 0

        # Determine if the player is labelled as active
        new_player_is_active = bool(
            new_player_inactivity
            < settings.NUMBER_OF_RATING_PERIODS_MISSED_TO_BE_INACTIVE
        )

        new_ratings[player] = {
            "player_ranking": None,
            "player_ranking_delta": None,
            "player_rating": new_player_rating,
            "player_rating_deviation": new_player_rating_deviation,
            "player_rating_volatility": new_player_rating_volatility,
            "player_inactivity": new_player_inactivity,
            "player_is_active": new_player_is_active,
        }

    # Filter all active players and sort by rating
    new_active_player_ratings = [
        (player, new_rating["player_rating"])
        for player, new_rating in new_ratings.items()
        if new_rating["player_is_active"]
    ]
    new_active_player_ratings.sort(key=lambda x: x[1], reverse=True)

    # Process new rankings and ranking changes
    num_active_players = len(new_active_player_ratings)

    # Keep track of the previous player's integer rating for ranking
    # ties
    last_integer_rating = None
    last_ranking = None

    for idx, player_tuple in enumerate(new_active_player_ratings, 1):
        # Unpack the player tuple
        player, rating = player_tuple

        integer_rating = round(rating)

        if (
            last_integer_rating is not None
            and last_integer_rating == integer_rating
        ):
            # Tie
            ranking = last_ranking
        else:
            last_integer_rating = integer_rating
            last_ranking = idx
            ranking = idx

        # Ranking
        new_ratings[player]["player_ranking"] = ranking

        # Ranking delta
        if player.ranking is None:
            new_ratings[player]["player_ranking_delta"] = (
                num_active_players - ranking + 1
            )
        else:
            new_ratings[player]["player_ranking_delta"] = (
                player.ranking - ranking
            )

    # Now save all ratings
    for player, ratings_dict in new_ratings.items():
        models.PlayerRatingNode.objects.create(
            player=player,
            rating_period=rating_period,
            ranking=ratings_dict["player_ranking"],
            ranking_delta=ratings_dict["player_ranking_delta"],
            rating=ratings_dict["player_rating"],
            rating_deviation=ratings_dict["player_rating_deviation"],
            rating_volatility=ratings_dict["player_rating_volatility"],
            inactivity=ratings_dict["player_inactivity"],
            is_active=ratings_dict["player_is_active"],
        )
