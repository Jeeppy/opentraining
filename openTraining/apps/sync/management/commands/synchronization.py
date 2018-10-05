from django.core.management import BaseCommand

from openTraining.apps.sync.tasks import synchronization


class Command(BaseCommand):
    help = "Synchronisation avec les services Strava"

    def handle(self, *args, **options):
        synchronization()
