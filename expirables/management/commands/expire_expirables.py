from django.core.management.base import BaseCommand
from ...expiration import run_expiration


class Command(BaseCommand):
    help = 'Expire all expirables'

    def handle(self, *args, **options):
        run_expiration()
