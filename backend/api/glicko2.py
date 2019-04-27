"""Contains functions for calculating player Glicko-2 ratings.

See http://www.glicko.net/glicko/glicko2.pdf for Glicko-2 implementation
details.
"""

from math import exp, log, pi, sqrt
from django.conf import settings

# Glicko-2 parameters
SCALE_FACTOR = 173.7178
EPSILON = 1e-6
TAU = settings.GLICKO2_SYSTEM_CONSTANT


# Functions to convert between Glicko and Glicko-2 ratings
def r_to_mu(r):
    return (r - settings.GLICKO2_BASE_RATING) / SCALE_FACTOR


def mu_to_r(mu):
    return mu * SCALE_FACTOR + settings.GLICKO2_BASE_RATING


def RD_to_phi(RD):
    return RD / SCALE_FACTOR


def phi_to_RD(phi):
    return phi * SCALE_FACTOR


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
    # Deal with degenerate case first when no games have been played by
    # the player
    if opponent_rs is None:
        RD_prime = phi_to_RD(sqrt(RD_to_phi(RD) ** 2 + sigma ** 2))

        return (r, RD_prime, sigma)

    # Calculate all ratings to Glicko-2 scale
    mu = r_to_mu(r)
    phi = RD_to_phi(RD)

    opponent_mus = [r_to_mu(opponent_r) for opponent_r in opponent_rs]
    opponent_phis = [RD_to_phi(opponent_RD) for opponent_RD in opponent_RDs]

    # Compute v and delta
    v = _v(mu, opponent_mus, opponent_phis)

    delta = _delta(v, mu, scores, opponent_mus, opponent_phis)

    # Compute new sigma value (Step 5 of Glicko-2 algorithm)
    f = f_closure(delta, v, sigma, phi)

    a = log(sigma ** 2)
    A = a

    if delta ** 2 > phi ** 2 + v:
        B = log(delta ** 2 - phi ** 2 - v)
    else:
        k = 1

        while f(a - k * TAU) < 0:
            k += 1

        B = a - k * TAU

    fA = f(A)
    fB = f(B)

    while abs(B - A) > EPSILON:
        C = A + (A - B) * fA / (fB - fA)
        fC = f(C)

        if fC * fB < 0:
            A = B
            fA = fB
        else:
            fA = fA / 2

        B = C
        fB = fC

    sigma_prime = exp(A / 2)

    # Compute new rating and rating deviation
    phi_star = sqrt(phi ** 2 + sigma_prime ** 2)

    phi_prime = 1 / sqrt(1 / phi_star ** 2 + 1 / v)
    mu_prime = mu + _delta(
        phi_prime ** 2, mu, scores, opponent_mus, opponent_phis
    )

    # Convert back to Glicko scale
    r_prime = mu_to_r(mu_prime)
    RD_prime = phi_to_RD(phi_prime)

    # Return the new ratings
    return (r_prime, RD_prime, sigma_prime)
