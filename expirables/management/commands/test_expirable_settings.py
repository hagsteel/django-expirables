from django.core.management.base import BaseCommand
from ...expiration import test_configuration


class Command(BaseCommand):
    help = 'Test expirables settings'

    def handle(self, *args, **options):
        test_configuration()
