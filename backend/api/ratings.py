"""Contains functions for calculating player ratings.

See http://www.glicko.net/glicko/glicko2.pdf for Glicko-2 implementation
details.
"""

from math import exp, log, pi, sqrt
from django.conf import settings
from . import models

# Glicko-2 parameters
SCALE_FACTOR = 173.7178
CONVERGENCE_TOLERANCE = 1e-6

# Customizable Glicko-2 parameters
BASE_RATING = settings.GLICKO2_BASE_RATING
BASE_RD = settings.GLICKO2_BASE_RD
BASE_VOLATILITY = settings.GLICKO2_BASE_VOLATILITY
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


def f_closure(delta, v, sigma, tau, phi):
    def f(x):
        return (
            exp(x)
            * (delta ** 2 - phi ** 2 - v - exp(x))
            / (2 * (phi ** 2 + v + exp(x)) ** 2)
            - (x - log(sigma ** 2)) / tau ** 2
        )

    return f
