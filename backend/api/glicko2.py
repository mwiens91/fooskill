"""Contains functions for calculating player Glicko-2 ratings.

See http://www.glicko.net/glicko/glicko2.pdf for Glicko-2 implementation
details.
"""

from math import exp, log, pi, sqrt
from django.conf import settings

# Glicko-2 parameters
SCALE_FACTOR = 173.7178
CONVERGENCE_TOLERANCE = 1e-6
TAU = settings.GLICKO2_SYSTEM_CONSTANT


# Functions used in Glicko-2 calculations
def _g(phi):
    return 1 / sqrt(1 + 3 * phi ** 2 / pi ** 2)


def _E(mu, mu_j, phi_j):
    return 1 / (1 + exp(-_g(phi_j) * (mu - mu_j)))


def _v(mu, mu_js, phi_js):
    summands = []

    for mu_j, phi_j in zip(mu_js, phi_js):
        g_j = _g(phi_j)
        E_j = _E(mu, mu_j, phi_j)

        summands.append(g_j ** 2 * E_j * (1 - E_j))

    return 1 / sum(summands)


def _delta(v, mu, s_js, mu_js, phi_js):
    summands = []

    for s_j, mu_j, phi_j in zip(s_js, mu_js, phi_js):
        summands.append(_g(phi_j) * (s_j - _E(mu, mu_j, phi_j)))

    return v * sum(summands)


def f_closure(delta, v, sigma, phi):
    def f(x):
        return (
            exp(x)
            * (delta ** 2 - phi ** 2 - v - exp(x))
            / (2 * (phi ** 2 + v + exp(x)) ** 2)
            - (x - log(sigma ** 2)) / TAU ** 2
        )

    return f


# The "main" rating calculating function
def calculate_player_rating(
    r, RD, sigma, opponent_rs=None, opponent_RDs=None, scores=None
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
        sigma: A float representing the player's rating volatility
        opponent_rs: A list of floats representing the ratings of each
            respective opponent per game.
        opponent_RDs: A list of floats representing the rating
            deviations of each respective opponent per game.
        scores: A list of floats representing the scores of each game.
            The scores are either 0 or 1, corresponding to a win by the
            opponent and a win by the player, respectively.

    Returns:
        A three-tuple containing the player's new rating, rating
        deviation, and rating volatility.
    """
    # TODO actually implement this
    return (420, 0.69, 0.5)
