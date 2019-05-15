"""Contains functions for calculating player Glicko ratings.

See http://www.glicko.net/glicko/glicko.pdf implementation details.
"""

from math import pi, sqrt
from django.conf import settings

# Glicko parameters
_c = 77.5
_q = 0.00575646273


# Functions used in Glicko-2 calculations
def _g(RD):
    return 1 / sqrt(1 + 3 * RD ** 2 / pi ** 2)


def _E(r, r_j, RD_j):
    return 1 / (1 + 10 ** (-_g(RD_j) * (r - r_j) / 400))


def _d(r, r_js, RD_js):
    summands = []

    for r_j, RD_j in zip(r_js, RD_js):
        g_j = _g(RD_j)
        E_j = _E(r, r_j, RD_j)

        summands.append(g_j ** 2 * E_j * (1 - E_j))

    return 1 / (_q ** 2 * sum(summands))


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
    # Intermediate RD value
    RD_int = min(sqrt(RD ** 2 + _c ** 2), settings.GLICKO_BASE_RD)

    # Deal with degenerate case first when no games have been played by
    # the player
    if opponent_rs is None:
        return (r, RD_int)

    # d is used in a bunch of calculations
    d = _d(r, opponent_rs, opponent_RDs)

    # Calulate r_prime and RD_prime
    summands = []

    for s_j, r_j, RD_j in zip(scores, opponent_rs, opponent_RDs):
        g_j = _g(RD_j)
        E_j = _E(r, r_j, RD_j)

        summands.append(g_j * (s_j - E_j))

    r_prime = r + _q / (1 / RD_int ** 2 + 1 / d ** 2) * sum(summands)
    RD_prime = sqrt(1 / (1 / RD_int ** 2 + 1 / d ** 2))

    # Return the new ratings
    return (r_prime, RD_prime)
