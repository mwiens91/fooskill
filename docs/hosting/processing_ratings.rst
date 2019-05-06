Processing ratings
==================

Most of the ratings and stats machinery in fooskill's backend is
automatic. Calculating rating periods, however, needs to either be run
manually or be scheduled periodically (with, for example, `cron
<https://en.wikipedia.org/wiki/Cron>`_).

There are three types of "nodes" fooskill uses to keep track of ratings
and statistics:

Player and matchup stats nodes
------------------------------

Player stats nodes contain stats related to a player. Matchup stats
nodes contain stats related to a matchup. Both of these types of nodes
are automatically generated when a new game is submitted, and
encapsulate the stats of the player or matchup up to the point in time
when the newly submitted game was played.

During development there may be occasion to reprocess stats from all
players over all games. This can be done with the following backend
command::

   ./manage.py reprocess_all_stats --reset-id-counter

The ``--reset-id-counter`` tells the database, after wiping all existing
stats nodes, to reset the ID counter for stats nodes back to 1, which is
optional and merely for aesthetics.

Player rating nodes
-------------------

Player rating nodes contain rating information related to a player for a
given rating period. These are created automatically when new rating
periods are processed. To process any new rating periods, run ::

   ./manage.py process_new_ratings

which will process any new rating periods that have yet to be evaluated.

As before, during development you might want to reprocess all rating
periods. This can be done with ::

   ./manage.py reprocess_all_ratings --reset-id-counter

where ``--reset-id-counter`` is optional and is identical to its
previous use, mentioned above.
