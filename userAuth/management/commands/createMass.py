from userAuth import factories
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        # create 10 of each using factories
        # factories.TaxPayerFactory.create_batch(10)
        # factories.TaxAccountantFactory.create_batch(10)
        factories.TaxFactory.create_batch(10)
