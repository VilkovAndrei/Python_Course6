
from django.core.management import BaseCommand

from main.services import start, send_mailing


class Command(BaseCommand):

    def handle(self, *args, **options):
        start()