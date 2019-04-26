"""Contains functions for calculating player ratings.

See http://www.glicko.net/glicko/glicko2.pdf for Glicko-2 implementation
details.
"""

from math import exp, pi, sqrt
from django.conf import settings
from . import models

# Glicko-2 parameters
SCALE_FACTOR = 173.7178

# Customizable Glicko-2 parameters
BASE_RATING = settings.GLICKO2_BASE_RATING
BASE_RD = settings.GLICKO2_BASE_RD
BASE_VOLATILITY = settings.GLICKO2_BASE_VOLATILITY
TAU = settings.GLICKO2_SYSTEM_CONSTANT


# Functions used in Glicko-2 calculations
def g(phi):
    return 1 / sqrt(1 + 3 * phi ** 2 / pi ** 2)


def E(mu, mu_j, phi_j):
    return 1 / (1 + exp(-g(phi_j) * (mu - mu_j)))


def v(mu, mu_js, phi_js):
    # Sanity check: The list of mus and phis passed in should be of the
    # same length.
    assert len(mu_js) == len(phi_js)

    # Build up list to sum over
    summands = []

    for mu_j, phi_j in zip(mu_js, phi_js):
        gj = g(phi_j)
        Ej = E(mu, mu_j, phi_j)

        summands.append(gj ** 2 * Ej * (1 - Ej))

    return 1 / sum(summands)

# TODO a few more functions needed here, but taking a break for now
