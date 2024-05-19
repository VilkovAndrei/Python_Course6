from main.management.commands.mailing import start, send_mailing
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        send_mailing()