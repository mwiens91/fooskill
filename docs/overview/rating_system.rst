Rating system
=============

fooskill uses either the `Glicko rating system`_ or the `Glicko-2 rating
system`_ to determine player ratings, and, by extension, player
rankings.

Rating periods
--------------

Unlike the `Elo rating system`_, ratings are not calculated game-by-game
with the Glicko algorithms. Instead, games are clustered into "rating
periods" that run for fixed amounts of time; then, all games in a rating
period are processed simultaneously.

Rating parameters
-----------------

**Glicko**

Glicko calculates two parameters for each player: their rating and their
rating deviation. Each player starts at rating of 1500. Like Elo, if you
win a game against a high rated opponent, your rating will increase more
than against an average rated opponent; most of the intuition gained
from the Elo algorithm will hold with the Glicko algorithm.

Each player will also have a rating deviation, which starts and is
capped at 350; it will decrease the more confident the system is that
the player is at their "true rating". A player's rating deviation gets
smaller the more active they are and the more predictable their game
outcomes are; conversely, their rating deviation gets larger the less
active they are and the more unpredictable their game outcomes are.

Glicko states that you can be confident that a player's "true rating"
:math:`r'` lies within

.. math::
   r - 2 \cdot RD \leq r' \leq r + 2 \cdot RD

where :math:`r` is their rating and :math:`RD` is their rating
deviation.

**Glicko-2**

Glicko-2 shares the rating and rating deviation parameters seen in
Glicko, and they behave as explained above. It also adds an additional
parameter: a player's rating volatility, which is a measure of how
volatile the player's game outcomes are. This parameter is in general
not interpretable to the same degree that the rating and rating
deviation parameters are.

Which rating algorithm should I use?
------------------------------------

Glicko-2 works best when you have ~15–20 games per player per rating
period. If you have significantly less than this game density, you won't
see any benefits of Glicko-2 and may be better off using Glicko.

.. _Elo rating system: https://en.wikipedia.org/wiki/Elo_rating_system
.. _Glicko rating system: http://www.glicko.net/glicko/glicko.pdf
.. _Glicko-2 rating system: http://www.glicko.net/glicko/glicko2.pdf
