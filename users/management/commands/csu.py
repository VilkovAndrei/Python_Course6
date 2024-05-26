from django.core.management import BaseCommand

from config.settings import PSQL_PSW
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@test.com',
            first_name='Admin',
            last_name='V',
            is_staff=True,
            is_superuser=True
        )

        user.set_password(PSQL_PSW)
        user.save()