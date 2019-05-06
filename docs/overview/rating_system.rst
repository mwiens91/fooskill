Rating system
=============

fooskill uses the `Glicko-2 rating system`_ to determine player ratings,
and, by extension, player rankings.

Rating periods
--------------

Unlike the `Elo rating system`_, ratings are not calculated game-by-game
with Glicko-2. Instead, games are clustered into "rating periods" that
run for fixed amounts of time; then, all games in a rating period are
processed simultaneously.

Rating parameters
-----------------

Glicko-2 calculates three parameters for players: their rating, rating
deviation, and rating volatility. Each player starts at 1500 rating.
Like Elo, if you win against a high rated opponent, your rating will
increase more than against an average rated opponent; most of the
intuition from Elo system will hold with Glicko-2.

Each player will also have a rating devation, which starts and is capped
at 350; it will decrease the more confident the system is that the
player is truly at their corresponding rating. So the rating deviation
gets smaller the more active you are and the more predictable your game
outcomes are; conversely, the rating devation gets larger the less
active you are and the more unpredictable your game outcomes are.

Glicko-2 states that you can be confident that a player's true rating
:math:`r'` lies within

.. math::
   r - 2 \cdot RD \leq r' \leq r + 2 \cdot RD

where :math:`r` is their current rating and :math:`RD` is their current
rating deviation.

A player's rating volatility is a measure of how volatile their outcomes
are, and the parameter is in general not interpretable beyond this
description.

.. _Elo rating system: https://en.wikipedia.org/wiki/Elo_rating_system
.. _Glicko-2 rating system: http://www.glicko.net/glicko/glicko2.pdf
