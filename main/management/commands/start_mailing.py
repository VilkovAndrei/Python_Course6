from main.management.commands.mailing import send_mailing
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        send_mailing()