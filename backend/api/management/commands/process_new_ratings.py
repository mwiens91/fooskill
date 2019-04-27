"""Custom command to process new ratings."""

from django.core.management.base import BaseCommand
from api.util import process_new_ratings


class Command(BaseCommand):
    help = "Calculates and creates new rating nodes and rating periods"

    def handle(self, *args, **options):
        process_new_ratings()
