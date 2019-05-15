"""Contains functions for calculating player Glicko ratings.

See http://www.glicko.net/glicko/glicko.pdf implementation details.
"""

from math import exp, log, pi, sqrt
from django.conf import settings


# The "main" rating calculating function
def calculate_player_rating(
    r, RD, opponent_rs=None, opponent_RDs=None, scores=None
):
    """Calculates a players rating given a set of games in a rating period.

    Note that the ith index of the opponent_* lists represents data from
    the ith game. So the order of elements in these lists is extremely
    important (it's instructive to view the opponent_* lists together as
    a 3 x m matrix, where m is the number of games played by the
    player). If no games have been played by the player for this rating
    period, all opponent_* variables will be set to None.

    Args:
        r: A float representing the player's rating.
        RD: A float representing the player's rating deviation.
        opponent_rs: A list of floats representing the ratings of each
            respective opponent per game.
        opponent_RDs: A list of floats representing the rating
            deviations of each respective opponent per game.
        scores: A list of floats representing the scores of each game.
            The scores are either 0 or 1, corresponding to a win by the
            opponent and a win by the player, respectively.

    Returns:
        A two-tuple containing the player's new rating and rating
        deviation.
    """
    raise NotImplementedError
