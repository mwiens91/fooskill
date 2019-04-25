"""Custom command to reprocess stats over all games."""

from django.core.management.base import BaseCommand
from api.util import reprocess_all_games


class Command(BaseCommand):
    help = (
        "Wipes all stats nodes and recreates/recalculates them over all games"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset_pk_counter",
            action="store_true",
            help="Reset pk counter back to 1 before recreating stats nodes.",
        )

    def handle(self, *args, **options):
        reprocess_all_games(reset_pk_counter=options["reset_pk_counter"])
